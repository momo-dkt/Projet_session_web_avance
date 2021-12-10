async function search(){
    
    const arrondissement=document.getElementById("arrondissement").value;
    
    
    
    let response = await fetch("/api/installations/"+arrondissement);
    let installations = await response.json()
    if(response.status==404){
       alert("Arrondissement inexistant");
       window.location= "/";
    
    }else{

      var output = "<h1>Installations</h1>";
      output += "<table>";  
    
      for (var i=0 in installations) {
        
        output += "<tr>"+"<td>" + installations[i].nom +"</td>" +"</tr>"; 
        
      }
    
      console.log(installations);
      output += "</table>";
      document.getElementById("installationsSeach").innerHTML=output;
      document.getElementById("list").innerHTML="";
   }
}

async function installation_details(){
    var installation=document.getElementById("installationsList").value;
    let response = await fetch("/api/installations/nom/"+installation);
    let installationJson = await response.json();
    if(response.status==400){
        alert("Installation inexistante");
        window.location= "/";
    }else{
      console.log(installationJson)
      let count = Object.keys(installationJson).length;
      console.log(count)
      let output;
      if(count==5){
        console.log("ENTER 5")
        output="<h1>"+installationJson.nom+"</h1>";
        output+="<ul>";
        output+="<li>"+"Arrondissement: "+ installationJson.arrondissement+"</li>";
        output+="<li>"+"Dernière mise à jour: "+ installationJson.Dernier_mise_a_jour+"</li>";
        if(installationJson.deblaye==0){
           output+="<li>"+"Deblayé:"+ " Non"+"</li>";
        }else if(installationJson.deblaye==1){
           output+="<li>"+"Deblayé:"+ " Oui"+"</li>";
        }

        if(installationJson.ouvert==0){
           output+="<li>"+"Ouvert:"+ " Non"+"</li>";
        }else if(installationJson.ouvert==1){
           output+="<li>"+"Ouvert:"+ " Oui"+"</li>";
        }
        output+="</ul>";
        document.getElementById("installationsSeach").innerHTML=output;
        document.getElementById("list").innerHTML="";

     }else if(count==3){
        console.log("ENTER 3")
        output="<h1>"+installationJson.nom+"</h1>";
        output+="<ul>";
        output+="<li>"+"Arrondissement: "+ installationJson.arrondissement+"</li>";
        output+="<li>"+"Dernière mise à jour: "+ installationJson.Dernier_mise_a_jour+"</li>";
        output+="</ul>";
        document.getElementById("installationsSeach").innerHTML=output;
        document.getElementById("list").innerHTML="";

     }else if(count==4){
        console.log("ENTER 4")
        output="<h1>"+installationJson.nom+"</h1>";
        output+="<ul>";
        output+="<li>"+"Arrondissement: "+ installationJson.arrondissement+"</li>";
        output+="<li>"+"Adresse: "+ installationJson.adresse+"</li>";
        output+="<li>"+"Type: "+ installationJson.type+"</li>";
        output+="</ul>";
        document.getElementById("installationsSeach").innerHTML=output;
        document.getElementById("list").innerHTML="";

     } 
    }
    

    



}