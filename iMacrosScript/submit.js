iimPlayCode('TAG POS=1 TYPE=SPAN ATTR=ID:bidBtn196');
iimPlayCode('WAIT SECONDS=1');
iimPlayCode('EVENT TYPE=CLICK SELECTOR="HTML>BODY>DIV:nth-of-type(5)>DIV:nth-of-type(11)>DIV" BUTTON=0');
iimPlayCode('EVENT TYPE=MOUSEDOWN SELECTOR="HTML>BODY>DIV:nth-of-type(5)>DIV:nth-of-type(14)>DIV:nth-of-type(5)>DIV:nth-of-type(2)>DIV>DIV>DIV:nth-of-type(2)" BUTTON=0')
for(let i=946;i<1230;i=i+10){
	let rndNum=(Math.random() * (0.12 - 0)).toFixed(2);
	let rndY=Math.floor(Math.random() * 11 + 576);	
	ret=iimPlayCode('WAIT SECONDS='+rndNum+'\nSET !TIMEOUT_STEP 1\nEVENT TYPE=MOUSEMOVE SELECTOR="HTML>BODY>DIV:nth-of-type(5)>DIV:nth-of-type(14)>DIV:nth-of-type(5)>DIV:nth-of-type(2)>DIV>DIV>DIV:nth-of-type(2)" POINT="('+i+','+rndY+')"')
	if(ret!=1){
		break;
	}
}
let submitBtn=window.content.document.querySelector('#submit-btn');
do{
	iimPlayCode('WAIT SECONDS=1');
}while(submitBtn.className=='tender-btn fr default-btn')
		iimDisplay('suc');
		//submitBtn.click();
