/** Offline smoke test: validates in-memory rendering and year/product filtering without a browser. */
const fs=require('fs'),vm=require('vm'),path=require('path');
const html=fs.readFileSync(path.join(__dirname,'..','02_Dashboard','Interactive_Complaint_Dashboard.html'),'utf8');
const code=html.slice(html.indexOf('<script>')+8,html.indexOf('</script>'));
const els={};
const mock={getElementById(id){return els[id]??(els[id]={id,innerHTML:'',value:'all',textContent:'',insertAdjacentHTML(){},addEventListener(){}})},querySelectorAll(){return []}};
const ctx=vm.createContext({document:mock,console});
vm.runInContext(code,ctx,{timeout:25000});
if(!els['ov-kpis'].innerHTML.includes('62,516')||!els['ov-kpis'].innerHTML.includes('96.06%'))throw Error('all-year metric mismatch');
if(!els['ti-long'].innerHTML.includes('4481803'))throw Error('long forwarding case missing');
console.log('PASS: all-year complaint/timeliness and longest interval case');
vm.runInContext("selYear='2022';render()",ctx,{timeout:25000});
if(!els['ov-kpis'].innerHTML.includes('12,953'))throw Error('year filter mismatch');
console.log('PASS: year 2022 filtering (12,953)');
vm.runInContext("selYear='all';selProd=String(P.indexOf('Checking or savings account'));render()",ctx,{timeout:25000});
if(!els['ov-kpis'].innerHTML.includes('24,814'))throw Error('product filter mismatch');
console.log('PASS: Checking/savings filtering (24,814)');
