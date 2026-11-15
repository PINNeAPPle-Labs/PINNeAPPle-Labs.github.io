/* Interactive reference solution to 1D heat equation.
 * Not a trained surrogate. Exact single-mode Dirichlet solution:
 * u(x,t) = A sin(pi*x/L) exp(-alpha*pi*pi*t/(L*L)).
 */
(() => {
  "use strict";
  const root = document.querySelector("[data-heat-demo]");
  if (!root) return;
  const canvas = root.querySelector("canvas");
  const ctx = canvas && canvas.getContext("2d");
  if (!ctx) return;
  const alpha = root.querySelector('[name="alpha"]');
  const time = root.querySelector('[name="time"]');
  const amplitude = root.querySelector('[name="amplitude"]');
  const output = root.querySelector("[data-heat-readout]");
  const csv = root.querySelector("[data-export]");
  const L = 1;
  const samples = () => Array.from({length:101}, (_,i) => {
    const x = i/100;
    const a = Number(alpha.value), t = Number(time.value), A = Number(amplitude.value);
    return [x, A*Math.sin(Math.PI*x/L)*Math.exp(-a*Math.PI*Math.PI*t/(L*L))];
  });
  function render() {
    const width = canvas.width, height = canvas.height, pad = 42;
    const data = samples();
    const maxY = Math.max(1,Number(amplitude.value));
    ctx.clearRect(0,0,width,height);
    ctx.fillStyle = "#0b1018"; ctx.fillRect(0,0,width,height);
    ctx.strokeStyle = "#1e2836";ctx.lineWidth = 1;
    ctx.beginPath();ctx.moveTo(pad,16);ctx.lineTo(pad,height-pad);ctx.lineTo(width-12,height-pad);ctx.stroke();
    ctx.strokeStyle = "#3dd6c4";ctx.lineWidth = 3;ctx.beginPath();
    data.forEach(([x,y],i) => {
      const px=pad+x*(width-pad-14), py=height-pad-(y/maxY)*(height-pad-28);
      if (i===0) ctx.moveTo(px,py); else ctx.lineTo(px,py);
    });
    ctx.stroke();
    ctx.fillStyle="#93a1b4";ctx.font="13px system-ui";
    ctx.fillText("x / L",width-50,height-12);ctx.fillText("u",16,22);
    const peak = Math.max(...data.map(p=>p[1]));
    output.textContent = "α = "+Number(alpha.value).toFixed(3)+" m²/s · t = "+Number(time.value).toFixed(2)+" s · max u = "+peak.toFixed(3);
  }
  [alpha,time,amplitude].forEach(el=>el.addEventListener("input",render));
  csv.addEventListener("click",()=>{
    const lines=["x_m,u"].concat(samples().map(row=>row.map(v=>v.toFixed(8)).join(",")));
    const blob=new Blob([lines.join("\n")+"\n"],{type:"text/csv"});
    const url=URL.createObjectURL(blob);
    const a=document.createElement("a");a.href=url;a.download="heat_equation_analytical.csv";a.click();
    URL.revokeObjectURL(url);
  });
  render();
})();