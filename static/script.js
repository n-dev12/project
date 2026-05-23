// 🤖 AI
function askAI(){
 const q = document.getElementById("aiQuestion").value;

 fetch("/ask_ai",{
  method:"POST",
  headers:{
   "Content-Type":"application/json"
  },
  body: JSON.stringify({question:q})
 })
 .then(res=>res.json())
 .then(data=>{
  document.getElementById("aiResponse").innerText = data.answer;
 })
 .catch(()=>{
  document.getElementById("aiResponse").innerText = "صار خطأ في الاتصال";
 });
}


// 🎇 3D BACKGROUND
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
 75,
 window.innerWidth/window.innerHeight,
 0.1,
 1000
);

const renderer = new THREE.WebGLRenderer({alpha:true});
renderer.setSize(window.innerWidth, window.innerHeight);

const bg = document.getElementById("bg3d");
if(bg){
 bg.appendChild(renderer.domElement);
}

const geo = new THREE.BufferGeometry();
const arr = new Float32Array(1500 * 3);

for(let i=0;i<arr.length;i++){
 arr[i] = (Math.random() - 0.5) * 20;
}

geo.setAttribute("position", new THREE.BufferAttribute(arr,3));

const mat = new THREE.PointsMaterial({
 size:0.03,
 color:0x38bdf8
});

const mesh = new THREE.Points(geo, mat);
scene.add(mesh);

camera.position.z = 5;

function animate(){
 requestAnimationFrame(animate);
 mesh.rotation.y += 0.0005;
 renderer.render(scene, camera);
}
animate();
document.addEventListener("DOMContentLoaded", function(){

  const textarea = document.getElementById("codeInput");
  const count = document.getElementById("count");

  if(!textarea || !count) return;

  function updateCount(){
    if(textarea.value.trim() === ""){
      count.innerText = "عدد الأسطر: 0";
    } else {
      const lines = textarea.value.split("\n").length;
      count.innerText = "عدد الأسطر: " + lines;
    }
  }

  textarea.addEventListener("input", updateCount);

  // تشغيل أولي
  updateCount();

});
const codeText = `function analyzeCode(project) {
  const results = await SmartAnalyzer.scan(project);

  return {
    errors: results.errors,
    vulnerabilities: results.security,
    suggestions: results.improvements
  };
}`;

let i = 0;
const speed = 30; // سرعة الكتابة

function typeWriter(){
  if(i < codeText.length){
    document.getElementById("typingCode").textContent += codeText.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}

window.onload = typeWriter;
function toggleCode(){

 const box = document.querySelector(".code-card");
 const btn = document.getElementById("toggleBtn");

 box.classList.toggle("expanded");

 if(box.classList.contains("expanded")){
   btn.innerText = "عرض أقل";
 }else{
   btn.innerText = "عرض المزيد";
 }

}