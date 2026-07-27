const resbox=document.getElementById("responsebox");

const scanbtn=document.getElementById("scanbtn");
scanbtn.addEventListener("click",function(){  
const searchbar=document.getElementById("searchbar").value;
getpy(searchbar);

const progresscont=document.getElementById("progresscont");
const progressbar=document.getElementById("progressbar");
/*
progresscont.style.display="block";
progressbar.style.width="0%"
 let progress=0
 const interval=setInterval( ()=>{
    progress+=10;

    progressbar.style.width=progress +"%";

    if (progress>= 90){
        clearInterval(interval);
    }
 },250);*/


async function getpy(searchval){  
    /*
    setTimeout(()=>{
        getpy(searchval);
    },5000);*/

  try{
    const searchpy=await fetch ("/scan",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
        url:searchval
        })
    });

    const relpy=await searchpy.json();
    
    /*
    lenearInterval(interval);
     progressbar.style.width="100%";
         setTimeout(() => {
            progresscont.style.display="none";
         },100);
  */
    console.log(relpy);
    resbox.innerHTML=
    `<div>
     <h3>${relpy.url}</h3>
     <p>${relpy.risk}</p>
     <p>Risk score:${relpy.score}%</p>
     <p>confidence:${relpy.confidence}%</p>
     <p>${relpy.reasons}</p>     
    </div>
    `;
    resbox.classList.remove("safe","warning","unsafe","caution","highrisk");
    if(relpy.risk==="highrisk"){
        resbox.classList.add("highrisk")
    }else if (relpy.risk==="caution"){
     resbox.classList.add("caution");
    }else if (relpy.risk==="unsafe"){
        resbox.classList.add("unsafe");
    }else if(relpy.risk==="suspecious"){
        resbox.classList.add("warning")
    }else{
        resbox.classList.add("safe");
    }
}
catch(error){
    console.error(error);
 }
}
});


const histpage=document.getElementById("histpage");
const histbtn=document.getElementById("histbtn");
histbtn.addEventListener("click", 
async function gethist(){
    try {
        if (histpage.style.display === "block") {
            histpage.style.display = "none";
            return;
        }

        const foundhist = await fetch("/history");
        const histres = await foundhist.json();

        histpage.style.display = "block";
        histpage.innerHTML = "";

        if (!histres.length) {
            histpage.innerHTML = "<p>No scan history yet.</p>";
            return;
        }

        histres.forEach(function (item) {
            histpage.innerHTML += `
            <div class="histcard">
                <p>URL:${item[0]}</p>
                <p>risk:${item[1]}</p>
                <p>score:${item[2]}%</p>
                <p>confidence:${item[3]}%</p>
                <p>reason:${item[4]}</p>
                <p>scanned:${item[5]}</p>
            </div>
            `;
        });
    } catch (error) {
        console.error("error loading history");
    }
});

//binary effect
function generateBinary(){
const binary=document.getElementById("binarystream");
if (!binary)return;

function createRow(){
    const row=document.createElement("div");
    row.classList.add("binary-row");

    let binaryString=" ";
    const length=40;
    for (let i = 0;i < length;i++){
        binaryString += Math.round(Math.random())+" ";
    }
    row.textContent = binaryString;
    binary.appendChild(row);

    setTimeout(()=> {
        row.remove();
    },4000);    
}

for(let i = 0;i<5;i++){
    setTimeout(createRow,i*800);
}

setInterval(createRow,800)
}
window.addEventListener("DOMContentLoaded",generateBinary);