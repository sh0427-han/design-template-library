const mode=document.body.dataset.mode;
document.querySelector('#lesson').innerHTML=`
<header><div class="kicker">생성형 AI · 개념</div><h1>검색 증강 생성의 흐름</h1><p class="subtitle"><b>검색 증강 생성(Retrieval-Augmented Generation, RAG)</b><br>질문과 관련된 외부 문서를 찾아, 생성 모델이 답변을 만드는 데 활용하는 방식</p></header>
<div class="rag-content">
<section class="diagram-panel" aria-labelledby="diagram-title"><div class="panel-label">준비와 사용</div><h2 id="diagram-title">저장한 문서를 질문할 때 찾아 사용</h2>
<svg class="pipeline" viewBox="0 0 1258 292" role="img" aria-labelledby="flow-title flow-desc"><title id="flow-title">문서 준비와 질문 응답 흐름</title><desc id="flow-desc">문서를 나누고 의미를 숫자로 표현하여 원문 조각과 함께 저장한다. 질문으로 저장소를 검색하고, 찾은 문서와 원래 질문을 생성 모델에 함께 제공하여 답변을 생성한다.</desc>
<g class="phase"><text x="0" y="23">01 문서 준비</text><text x="0" y="171">02 질문 응답</text></g>
<g class="box" data-node="documents"><rect x="160" y="0" width="190" height="74" rx="10"/><text x="255" y="30">외부 문서</text><text class="sub" x="255" y="56">답변에 참고할 자료</text></g>
<g class="box" data-node="chunks"><rect x="394" y="0" width="190" height="74" rx="10"/><text x="489" y="30">문서 나누기</text><text class="sub" x="489" y="56">찾기 좋은 크기의 조각</text></g>
<g class="box" data-node="representation"><rect x="628" y="0" width="210" height="74" rx="10"/><text x="733" y="30">검색할 표현 만들기</text><text class="sub" x="733" y="56">의미를 숫자로 표현</text></g>
<g class="box storage" data-node="store"><rect x="882" y="0" width="220" height="74" rx="10"/><text x="992" y="30">문서 저장소</text><text class="sub" x="992" y="56">원문 조각 + 검색 표현</text></g>
<g class="arrows"><path d="M353.5 37 H390.5 M384.5 32 L390.5 37 L384.5 42"/><path d="M587.5 37 H624.5 M618.5 32 L624.5 37 L618.5 42"/><path d="M841.5 37 H878.5 M872.5 32 L878.5 37 L872.5 42"/></g>
<path class="transfer" d="M992 77.5 V108 H425 V144.5 M420 138.5 L425 144.5 L430 138.5"/><text class="transfer-label" x="690" y="101">저장한 문서에서 찾기</text>
<g class="box" data-node="question"><rect x="160" y="148" width="140" height="80" rx="10"/><text x="230" y="183">질문</text><text class="sub" x="230" y="208">알고 싶은 내용</text></g>
<g class="box" data-node="search"><rect x="344" y="148" width="162" height="80" rx="10"/><text x="425" y="183">관련 문서 검색</text><text class="sub" x="425" y="208">질문을 검색에 사용</text></g>
<g class="box bundle" data-node="bundle"><rect x="550" y="148" width="230" height="80" rx="10"/><text x="665" y="183">원래 질문 + 찾은 문서</text><text class="sub" x="665" y="208">생성 모델에 함께 제공</text></g>
<g class="box" data-node="model"><rect x="824" y="148" width="180" height="80" rx="10"/><text x="914" y="183">생성 모델</text><text class="sub" x="914" y="208">자료를 참고해 작성</text></g>
<g class="box answer" data-node="answer"><rect x="1048" y="148" width="160" height="80" rx="10"/><text x="1128" y="183">답변</text><text class="sub" x="1128" y="208">생성된 설명</text></g>
<g class="arrows"><path d="M303.5 188 H340.5 M334.5 183 L340.5 188 L334.5 193"/><path d="M509.5 188 H546.5 M540.5 183 L546.5 188 L540.5 193"/><path d="M783.5 188 H820.5 M814.5 183 L820.5 188 L814.5 193"/><path d="M1007.5 188 H1044.5 M1038.5 183 L1044.5 188 L1038.5 193"/><path d="M230 231.5 V270 H665 V231.5 M660 237.5 L665 231.5 L670 237.5"/></g><text class="branch-label" x="440" y="261">원래 질문도 전달</text>
</svg></section>
<div class="notes"><p><b>재학습과의 차이</b> 재학습은 모델의 학습된 내부 값을 바꿈.<br>이 흐름은 모델을 재학습하지 않고 외부 문서를 검색해 사용.</p><p><b>정확성의 한계</b> 검색이 관련 자료를 놓치거나 모델이 잘못 해석할 수 있음.<br>검색을 사용해도 답변의 정확성이 자동 보장되지는 않음.</p></div>
<div class="ref-takeaway"><strong>핵심 연결</strong><span>문서를 미리 준비하고, 질문할 때 찾은 내용을 답변의 참고 자료로 제공</span></div>
</div><footer class="footer"><span>검색 증강 생성 · 개념</span><span>01 / 01</span></footer>`;
const target=mode==='scroll'?'slides':'scroll';
document.querySelector('#switch').href=target+'.html#rag';
document.querySelector('#switch').textContent=mode==='scroll'?'Slide 보기':'Scroll 보기';
function fit(){const scale=mode==='slide'?Math.min(1,(innerWidth-40)/1440,(innerHeight-88)/810):Math.min(1,(innerWidth-48)/1440);document.querySelector('#lesson').style.zoom=scale;}
fit();addEventListener('resize',fit);history.replaceState(null,'','#rag');
document.fonts.ready.then(()=>{document.body.dataset.ready='true'});
