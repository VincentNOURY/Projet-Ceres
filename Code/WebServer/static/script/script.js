function ajoute(){
  let table = document.getElementsByName("affichage")[0];
  let infos = document.forms.capteurs;
  let tr = document.createElement('tr');
  console.log(infos.length);
  for (i = 0; i < infos.length - 1; i++){
    let td = document.createElement('td');
    td.textContent = infos[i].value;
    tr.appendChild(td);
  }
  table.appendChild(tr);
}

async function getMeteo(){
  await sleep(10);
  fetch("../pluie.json")
    .then((response) => response.json())
    .then(function (data){
      let meteo = document.querySelector("#pluie");
      for (let i = 0; i < 8; i++){
        let index = (i*3 + 1).toString();
        
        const td1 = document.createElement("td");
        td1.textContent=index + "H";

        if (index.length < 2){
          index = "0" + index;
        }
        let tr = document.createElement('tr');

        const td2 = document.createElement('td');
        td2.textContent=data["0"][index];

        const td3 = document.createElement('td');
        td3.textContent=data["1"][index];

        const td4 = document.createElement('td');
        td4.textContent=data["2"][index];

        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);

        meteo.appendChild(tr);
      }

  })

  fetch("../temperature.json")
    .then((response) => response.json())
    .then(function (data){
      let meteo = document.querySelector("#temperature");
      for (let i = 0; i < 8; i++){
        let index = (i*3 + 1).toString();

        const td1 = document.createElement("td");
        td1.textContent=index + "H";

        if (index.length < 2){
          index = "0" + index;
        }
        let tr = document.createElement('tr');

        const td2 = document.createElement('td');
        td2.textContent=data["0"][index];

        const td3 = document.createElement('td');
        td3.textContent=data["1"][index];

        const td4 = document.createElement('td');
        td4.textContent=data["2"][index];

        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);

        meteo.appendChild(tr);
      }

  })
}
getMeteo();

function sleep(ms){
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function time(){
  await sleep(1);
  while (true){
    date = new Date();
    str = date.getHours() + " h " + date.getMinutes() + " m " + date.getSeconds() + " s";
    document.querySelector("#time").innerHTML = str;
    await sleep(1000);
  }
}

time();
