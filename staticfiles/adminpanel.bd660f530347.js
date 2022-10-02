
// Sidebar Toggle
document.getElementById("sidebarToggleMenu").addEventListener("click", ()=>{
    document.getElementById("accordionSidebar").classList.toggle("toggled");
    if(document.getElementById("accordionSidebar").classList.contains("toggled")){
        document.getElementById("Toggle1").classList.add("d-none");
        document.getElementById("Toggle2").classList.remove("d-none");
    }else{
        document.getElementById("Toggle2").classList.add("d-none");
        document.getElementById("Toggle1").classList.remove("d-none");
    }
})



const dashboard = document.querySelector(".link-1");
const unpaid_agree = document.querySelector(".link-2");
const detail_page = document.querySelector(".detail-page");

const nav_items = document.querySelectorAll(".nav-item");
const pages = document.querySelectorAll(".page");
const page_title = document.querySelector(".page-name");
var current_page = 0;

dashboard.addEventListener("click", loadDashboard);
unpaid_agree.addEventListener("click", loadUnpaid_Agree);


const close_detail_page = document.getElementById("close-detail-page");

close_detail_page.addEventListener("click", CloseDetailPage)

function CloseDetailPage(){
    pages[2].classList.add("d-none");
    pages[prev_page].classList.remove("d-none");
    nav_items[prev_page].classList.add("active");
    current_page = prev_page;
    get_unpaid_agreements();
}

function load_detail_page(){
    if(pages[2].classList.contains("d-none")){
        pages[2].classList.remove("d-none");
    }
    if(current_page != 2){
        pages[current_page].classList.add("d-none");
    }
    nav_items[current_page].classList.remove("active");
    prev_page = current_page;
    current_page = 2;
}



function loadDashboard(){
    if(pages[0].classList.contains("d-none")){
        pages[0].classList.remove("d-none");
    }
    if(current_page != 0){
        pages[current_page].classList.add("d-none");
    }
    nav_items[current_page].classList.remove("active");
    current_page = 0;
    nav_items[current_page].classList.add("active");
    page_title.innerHTML = "Dashboard";
}

function loadUnpaid_Agree(){
    if(pages[1].classList.contains("d-none")){
        pages[1].classList.remove("d-none");
    }
    if(current_page != 1){
        pages[current_page].classList.add("d-none");
    }
    nav_items[current_page].classList.remove("active");
    current_page = 1;
    nav_items[current_page].classList.add("active");
    
    get_unpaid_agreements();
}



function detail_page_info(participant_id){
    $("#spinner").removeClass("d-none");
    $("#spinner").addClass("d-flex");

    $("#team_name").html("");
    $("#team_member_no").html("");
    $("#team_leader").html("");
    $("#team_leader_phone").html("");
    $("#team_leader_email").html("");
    $("#team_member_names").html("");
    $("#payment_status").html("");
    $("#college_name").html("");


    


    const url = "/single_team/" + participant_id + "/";
    $.get(url, (data, status)=>{
        if(status=="success"){
            id = data.pk;
            info = data[0].fields

            $("#team_name").text(info.event_participated);
            $("#team_member_no").text(info.number_of_members);
            $("#team_leader").text(info.leader);

            $("#team_leader_phone").text(info.leader_phone_number);
            $("#team_leader_phone").attr("href", "https://wa.me/"+info.leader_phone_number );

            $("#team_leader_email").text(info.leader_email);
            $("#team_leader_email").attr("href", "mailto:"+info.leader_email);

            $("#payment_status").html(info.payment_status);
            $("#college_name").text(info.college_name);

            if(info.name_of_members){
                const team_member_names = info.name_of_members.split("|")
                for(let member of team_member_names){
                    const child = `<li><span class=" text-start d-inline">${ member }</span></li>`
                    $("#team_member_names").append(child);
                }
            }else{
                $("#team_member_names").text("No Team Members");
            }

            $("#spinner").removeClass("d-flex");
            $("#spinner").addClass("d-none");

            window.scrollTo(0, 0);
            load_detail_page();
            
        }
    })

}



function player_detail_page_info(participant_id){
    $("#spinner").removeClass("d-none");
    $("#spinner").addClass("d-flex");

    $("#participant_name").html("")
    $("#player_phone").html("")
    $("#player_email").html("")
    $("#participant_college_name").html("")
    $("#participant_payment_status").html("")
    // $("#participant_name").html("")

    const url = "/single_player/" + participant_id + "/";
    $.get(url, (data, status)=>{
        if(status=="success"){
            id = data.pk;
            info = data[0].fields

            $("#participant_name").text(info.player_name);
            $("#player_phone").text(info.player_phone_number);
            $("#player_phone").attr("href", "https://wa.me/"+info.player_phone_number )

            $("#player_email").text(info.player_email);
            $("#player_email").attr("href", "mailto:"+info.player_email);

            $("#participant_college_name").text(info.college_name);
            $("#participant_payment_status").text(info.payment_status);


            $("#spinner").removeClass("d-flex");
            $("#spinner").addClass("d-none");

            window.scrollTo(0, 0);
            load_detail_page();
            
        }
    })

}





var myinterval;

function get_teams(){

    CURRENT_AGREEMENT_NUMBER = $("#participant-table tr").length;
    let TOTAL_AGREEMENT_NUMBER = 0;

    $.get("/cout_data/", function(data, status, xhr){
        if(status == "success"){
            TOTAL_AGREEMENT_NUMBER = parseInt(data);

            let MISSING_AGREEMENTS = TOTAL_AGREEMENT_NUMBER - CURRENT_AGREEMENT_NUMBER;

            if(MISSING_AGREEMENTS > 0){

                clearInterval(myinterval);
                let url = "/data_number/" + MISSING_AGREEMENTS + "/"
                $.get(url, (data, status)=>{
                    if(status == "success"){
                        console.log(data[0].fields);
                        data.forEach(team => {
                            let child = `<tr>
                                            <td>${ team.pk }</td>
                                            <td>${ team.fields.team_name }</td>
                                            <td>
                                                <a target="_blank" class="d-inline ml-3 text-decoration-none" href="mailto:riteshthawkar2003@gmail.com">
                                                    <span class="d-inline">${ team.fields.leader_email }</span>
                                                </a>
                                            </td>
                                            <td>
                                                <a target="_blank" class="d-inline ml-3 text-decoration-none" href="https://wa.me/919552361592">
                                                    +91<span class="d-inline">${ team.fields.leader_phone_number }</span>
                                                </a>
                                            </td>
                                            <td>${ team.fields.payment_status }</td>
                                            <td class="page-detail text-primary" style="cursor:pointer;" onclick="detail_page_info( ${ team.pk } )">Details</td>
                                        </tr>`
                                
                            $("#participant-table").prepend(child);
                        });
                    }
                })
                CURRENT_AGREEMENT_NUMBER += MISSING_AGREEMENTS;
                myinterval = setInterval(get_teams, 6000)
            }
        }
    })
}

myinterval = setInterval(get_teams, 6000);









// Unpaid Participants

function get_unpaid_agreements(){
    CURRENT_AGREEMENT_NUMBER = $("#unpaid-teams-table tr").length;
    let TOTAL_AGREEMENT_NUMBER = 0;

    $.get("/unpaid_cout_data/", function(data, status, xhr){
        if(status == "success"){
            TOTAL_AGREEMENT_NUMBER = parseInt(data);

            let MISSING_AGREEMENTS = TOTAL_AGREEMENT_NUMBER - CURRENT_AGREEMENT_NUMBER;

            if(MISSING_AGREEMENTS > 0){

                let url = "/unpaid_data_number/" + MISSING_AGREEMENTS + "/"
                $.get(url, (data, status)=>{
                    if(status == "success"){
                        data.forEach(team => {
                            let child = `<tr>
                                            <td>${ team.pk }</td>
                                            <td>${ team.fields.team_name }</td>
                                            <td>
                                                <a target="_blank" class="d-inline ml-3 text-decoration-none" href="mailto:riteshthawkar2003@gmail.com">
                                                    <span class="d-inline">${ team.fields.leader_email }</span>
                                                </a>
                                            </td>
                                            <td>
                                                <a target="_blank" class="d-inline ml-3 text-decoration-none" href="https://wa.me/919552361592">
                                                    +91<span class="d-inline">${ team.fields.leader_phone_number }</span>
                                                </a>
                                            </td>
                                            <td>${ team.fields.payment_status }</td>
                                            <td class="page-detail text-primary" style="cursor:pointer;" onclick="detail_page_info( ${ team.pk } )">Details</td>
                                        </tr>`
                                
                            $("#unpaid-teams-table").prepend(child);
                        });
                    }
                })
            }
        }
    })
}


