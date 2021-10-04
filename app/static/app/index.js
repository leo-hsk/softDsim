/* Staff Picker */


function pickerAdd(n) {
    x._data.staff[n] += "•";
}

function pickerSub(n) {
    const str = x._data.staff[n];
    x._data.staff[n] = str.substring(0, str.length - 1)
}

/* Meetings */
function addMeeting() {
    if (x._data.meetings < 8) {
        x._data.meetings += 1
    }
}

function subMeeting() {
    if (x._data.meetings > 0) {
        x._data.meetings -= 1
    }

}


function toggleVisibility(elId){
    const element = document.getElementById(elId);
    if (element.style.display == 'none'){
        element.style.display = 'block'
    } else {
        element.style.display = 'none'
    }
}

/* Activity Distribution Chart */

function calculateActivityLength(meetings, trainings) {
    let m = (meetings / 40) * 100;
    let t = (trainings / 40) * 100;
    let d = 100 - m - t;
    return [d, m, t]
}


function makeActivityChart(length) {
    const children = document.getElementById("activity-distribution-container").children;
    const colors = ['#55AAFF', '#AAFF55', '#FF55AA']
    for (let i of [0, 1, 2]) {
        children[i].style.backgroundColor = colors[i]
        children[i].style.width = "" + length[i] + "%"
    }
}


function all_required_actions_done(){
    let t = true;
    for (const c of document.getElementsByClassName('req')) {
        let active = false;
        for (const li of c.nextElementSibling.childNodes){
            if (li.childNodes[0].classList.contains('active-button')){
                active = true;
            }
        }
        if (active === false){
            t = false
        }
    }
    return t;
}

function set_continue_button(){
    document.getElementById('continue-button').disabled = !all_required_actions_done();
}


document.addEventListener("click", () =>{
    set_continue_button()
})