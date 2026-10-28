"""Independent exact arithmetic checks; browser evidence belongs to verify_runtime.py.

The earlier content-injection report/previews are historical and are not overwritten.
Expected values are derived in Python, never from the production JavaScript.
"""
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from pathlib import Path
import json, subprocess

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'data.json').read_text())
IDS = ('identity', 'mean', 'edge')


def reference(input_rows, kernel, denominator):
    return [[Fraction(sum(input_rows[r+i][c+j] * kernel[i][j]
                         for i in range(3) for j in range(3)), denominator)
             for c in range(len(input_rows[0])-2)]
            for r in range(len(input_rows)-2)]


def displayed(value):
    value = Fraction(value)
    rounded = (Decimal(value.numerator) / Decimal(value.denominator)).quantize(
        Decimal('.01'), rounding=ROUND_HALF_UP)
    return str(int(rounded)) if rounded == int(rounded) else f'{rounded:.2f}'


def color(value):
    value = Fraction(value)
    anchor = (38,166,161) if value < 0 else (49,104,200)
    amount = min(Fraction(1), abs(value) / 36)
    channels = []
    for channel in anchor:
        exact = 255 + (channel - 255) * amount
        floor, remainder = divmod(exact.numerator, exact.denominator)
        channels.append(floor + (2 * remainder >= exact.denominator))
    return 'rgb(' + ', '.join(map(str, channels)) + ')'


def fixture_data():
    result = {'default': DATA}
    for name, matrix in {
        'zero': [[0] * 7 for _ in range(7)],
        'nine': [[9] * 7 for _ in range(7)],
        'ramp': [[(r + 2*c) % 10 for c in range(7)] for r in range(7)],
        'impulse': [[9 if (r,c)==(3,3) else 0 for c in range(7)] for r in range(7)],
    }.items():
        data = deepcopy(DATA); data['input'] = matrix; result[name] = data
    return result


def verify():
    fixtures = fixture_data()
    source = r'''const fs=require('fs'),M=require('./model.js'),fixtures=JSON.parse(fs.readFileSync(0,'utf8'));
const cases=[];for(const [fixture,d] of Object.entries(fixtures))for(const id of ['identity','mean','edge']){const state=M.evaluate(d,id);cases.push({fixture,id,state,colors:state.output.map(r=>r.map(M.colorFor)),display:state.output.map(r=>r.map(M.formatValue))});}
const asymmetric={input:[[1,2,3,4,5],[2,4,6,8,9],[3,6,9,2,4],[4,8,2,6,1]],kernel:[[1,2,0],[0,-1,0],[0,0,3]],divisor:2};
const direction={fixture:asymmetric,result:M.correlate(asymmetric.input,asymmetric.kernel,asymmetric.divisor)};
const colors=[-72,-36,-18,0,18,36,72].map(value=>({value,color:M.colorFor(value)}));
const base=fixtures.default,copy=()=>JSON.parse(JSON.stringify(base));
const invalid=[];
invalid.push(null,{}, {...copy(),input:[]}, {...copy(),input:Array(6).fill(Array(7).fill(0))});
for(const value of [-1,10,.1,NaN,Infinity]){const d=copy();d.input[0][0]=value;invalid.push(d);}
for(const value of [0,-1,1.5]){const d=copy();d.kernels.mean.divisor=value;invalid.push(d);}
{const d=copy();d.kernels.mean.name='';invalid.push(d);}
{const d=copy();d.kernels.edge.numerators[0][0]=NaN;invalid.push(d);}
let invalidData=0;for(const d of invalid){try{M.validateData(d);}catch(e){invalidData++;}}
const badIds=['',null,'sobel','__proto__'];let invalidIds=0;for(const id of badIds){try{M.evaluate(base,id);}catch(e){invalidIds++;}}
const invalidCorrelations=[()=>M.correlate([],[[0,0,0],[0,1,0],[0,0,0]]),()=>M.correlate([[0,0],[0,0],[0,0]],[[0,0,0],[0,1,0],[0,0,0]]),()=>M.correlate([[0,0,0],[0,0],[0,0,0]],[[0,0,0],[0,1,0],[0,0,0]]),()=>M.correlate(base.input,[[1]],1),()=>M.correlate(base.input,base.kernels.mean.numerators,0),()=>M.correlate(base.input,base.kernels.mean.numerators,-1),()=>M.correlate(base.input,Array(3).fill(Array(3).fill(Number.MAX_SAFE_INTEGER)))];let invalidCorrelation=0;for(const fn of invalidCorrelations){try{fn();}catch(e){invalidCorrelation++;}}
console.log(JSON.stringify({cases,direction,colors,invalidData,invalidDataTotal:invalid.length,invalidIds,invalidCorrelation}));'''
    actual = json.loads(subprocess.check_output(['node','-e',source],cwd=ROOT,
                                               input=json.dumps(fixtures),text=True))
    for case in actual['cases']:
        data, kid = fixtures[case['fixture']], case['id']; kernel = data['kernels'][kid]
        expected = reference(data['input'], kernel['numerators'], kernel['divisor'])
        state = case['state']; divisor = kernel['divisor']
        assert state['outputNumerators'] == [[int(value*divisor) for value in row] for row in expected]
        assert all(abs(state['output'][r][c] - float(expected[r][c])) < 1e-12 for r in range(5) for c in range(5))
        assert case['colors'] == [[color(value) for value in row] for row in expected]
        assert case['display'] == [[displayed(value) for value in row] for row in expected]
        patch = [row[1:4] for row in data['input'][2:5]]
        products = [[patch[r][c]*kernel['numerators'][r][c] for c in range(3)] for r in range(3)]
        focus = state['focus']; assert focus['patch'] == patch and focus['products'] == products
        assert focus['numerator'] == int(expected[2][1]*divisor) and focus['denominator'] == divisor
        assert focus['display'] == displayed(expected[2][1])
        assert abs(focus['raw'] - float(expected[2][1])) < 1e-12
    direction = actual['direction']; data = direction['fixture']
    expected = reference(data['input'],data['kernel'],data['divisor'])
    reversed_kernel = [row[::-1] for row in data['kernel'][::-1]]
    assert expected != reference(data['input'],reversed_kernel,data['divisor'])
    assert direction['result']['outputNumerators'] == [[int(v*data['divisor']) for v in row] for row in expected]
    assert all(c['color'] == color(c['value']) for c in actual['colors'])
    assert actual['invalidData'] == actual['invalidDataTotal'] == 14
    assert actual['invalidIds'] == 4 and actual['invalidCorrelation'] == 7
    default = {kid:reference(DATA['input'],DATA['kernels'][kid]['numerators'],DATA['kernels'][kid]['divisor']) for kid in IDS}
    assert [default[kid][2][1] for kid in IDS] == [6,Fraction(51,9),28]
    assert min(map(min,default['edge'])) == -28 and max(map(max,default['edge'])) == 28
    assert len({tuple(v for row in matrix for v in row) for matrix in default.values()}) == 3
    return {'status':'passed','oracle':'Independent Python integer/Fraction and exact decimal display rounding',
            'filter_data_cases':len(actual['cases']),'verified_output_cells':len(actual['cases'])*25,
            'asymmetric_correlation_differs_from_flipped_kernel':True,'color_endpoints_and_clipping':actual['colors'],
            'invalid_data_rejected':actual['invalidData'],'invalid_ids_rejected':actual['invalidIds'],
            'invalid_correlations_rejected':actual['invalidCorrelation'],
            'focus':{'identity':'6','mean':'51/9 ≈ 5.67','edge':'28'},
            'historical_injection_evidence_not_overwritten':True}


def main():
    report = verify(); target = ROOT/'review/arithmetic-validation.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f"PASS independent arithmetic: {report['filter_data_cases']} cases / {report['verified_output_cells']} output cells / signed colors, direction and invalid inputs")


if __name__ == '__main__': main()
