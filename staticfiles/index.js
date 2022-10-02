

// Participation Form Page
$(document).ready(()=>{
if(document.getElementById("event_type_1".checked)){
    $("#number_of_members").val(1);
}
})
$("#event_type_1").change(()=>{
$("#number_of_members").val(1);
})



document.getElementById("add_member_button").addEventListener("click", ()=>{

    const team_members = parseInt($("#number_of_members").val());
    const allowedMembers = parseInt($("#number_of_members").attr("max"));

    if(team_members <= allowedMembers){

        if(document.getElementById("add_member_container").classList.contains("hidden")){
            document.getElementById("add_member_container").classList.remove("hidden");
        }

        if(! $("#membersWarning").hasClass("hidden")){
          $("#membersWarning").addClass("hidden");
        }

        $("#add_member").empty()
        for (let i=0; i<team_members; i++){
            const child = `<div class="w-full px-3 mb-5">
                            <label class="block uppercase tracking-wide text-gray-700 text-sm font-bold mb-2" for="member_full_name">
                                Full Name of Team Member ${i+1}
                            </label>
                            <input class="team_member_name appearance-none block w-full text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="member_full_name_${i+1}" type="text" placeholder="Team Member Name" required>
                            </div>`
            $("#add_member").append(child);
        }
    }else{
        $("#membersWarning").toggleClass("hidden");
        $("#number_of_members").val("");
        if(!document.getElementById("add_member_container").classList.contains("hidden")){
            document.getElementById("add_member_container").classList.add("hidden");
        }
    }

})


function makeName () {
                
    var fields = document.querySelectorAll(".team_member_name");

    var values = [];
    for(let i=0; i<fields.length; i++){
      values.push(fields[i].value ? fields[i].value : "");
    }
    
    $('#name_of_members').val('');
    $('#name_of_members').val(values.join('|'));
};


if(document.getElementById("event_type_2").checked){
    document.getElementById("member_choose").classList.toggle("hidden");
}
document.getElementById("event_type_2").addEventListener("change", ()=>{
      document.getElementById("member_choose").classList.toggle("hidden");
})
document.getElementById("event_type_1").addEventListener("change", ()=>{
      document.getElementById("member_choose").classList.add("hidden");
})