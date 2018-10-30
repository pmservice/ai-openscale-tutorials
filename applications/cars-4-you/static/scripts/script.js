let logoImage = document.getElementById("logoimg")
let textInput = document.getElementById('user-text');
let userComment = document.getElementById("user-comment");

let verySadFaceImage = document.getElementById('very-sad');
let sadFaceImage = document.getElementById('sad');
let neutralFaceImage = document.getElementById('neutral');
let happyFaceImage = document.getElementById('happy');
let veryHappyFaceImage = document.getElementById('very-happy');

let responseFace = document.getElementById("response-face");
let sendButton = document.getElementById("send-button");
let feedbackComment = document.getElementById("feedback-comment");
let questionBox = document.getElementById("question");
let responseBox = document.getElementById("response");
let sidebar = document.getElementById("sidebar");
let modelSidebar = document.getElementById("sidebar-models");
let errorPanel = document.getElementById("error-message");
let saveButton = document.getElementById("sidebar-save");
let cancelButton = document.getElementById("sidebar-cancel");
let saveModelButton = document.getElementById("sidebar-model-save");
let cancelModelButton = document.getElementById("sidebar-model-cancel");
let customerName = document.getElementById("cust-name");
let firstName = document.getElementById("first-name-input");
let secondName = document.getElementById("last-name-input");
let genderInput = document.getElementById("gender-input");
let ageInput = document.getElementById("age-input");
let statusInput = document.getElementById("status-input");
let childrenInput = document.getElementById("children-input");
let carownerInput = document.getElementById("owner-input");
let activeInput = document.getElementById("active-input");
let areaActionSelection = document.getElementById("area-input");

let payloadData = {
    "Customer_Service": "",
    "Customer_Status": "Inactive",
    "Gender": "Male",
    "Status": "S",
    "Children": 2,
    "Age": 36,
    "Customer": "Active",
    "Car_Owner": "Yes",
    "Satisfaction": -1
};

let userData = {
    "username": "John",
    "lastname" : "Smith",
    "payload": payloadData
};

let scoringPayload = {
    "deployment" : {},
    "payload" : {}
};

let deployments = [];
let selectedFace = null;

get_cars4u_deployments();

cancelButton.onclick = function () {
    reset_sidebar();
    show_hide_sidebar();
};

saveButton.onclick = function () {
    update_customer_name();
    show_hide_sidebar();
};

cancelModelButton.onclick = function(){
    show_hide_model_sidebar();
};

saveModelButton.onclick = function() {
    show_hide_model_sidebar();
};

logoImage.onclick = function () {
    location.reload();
};

sendButton.onclick = function () {
    let comment = textInput.value;
    userComment.innerHTML = comment;

    send_request(comment);
};

verySadFaceImage.addEventListener('click', select_sad);
sadFaceImage.addEventListener('click', select_sad);
neutralFaceImage.addEventListener('click', select_happy);
happyFaceImage.addEventListener('click', select_happy);
veryHappyFaceImage.addEventListener('click', select_happy);

document.getElementById("avatar-button").addEventListener('click', show_hide_sidebar);
document.getElementById("user-welcome").addEventListener('click', show_hide_sidebar);
document.getElementById("logout-button").addEventListener('click', function() { location.reload(); });
document.getElementById("model-button").addEventListener('click', show_hide_model_sidebar);


function handleClick(element) {
    let clickedImage = element.target;

    deselect_faces();

    if (clickedImage.src.includes('selected')){
        clickedImage.src = "/static/images/" + clickedImage.id + ".svg";
    }
    else {
        clickedImage.src = "/static/images/selected_" + clickedImage.id + ".svg";
        selectedFace = clickedImage;
    }
}


function get_cars4u_deployments() {
    $.get(
        "/deployments",
        function (data) {
            let currentValue = areaActionSelection.value;
            areaActionSelection.innerHTML = "";
            if (data.length === 0){
                let opt = document.createElement('option');
                opt.value = '';
                opt.innerHTML = "< no CARS4U deployments >";
                areaActionSelection.appendChild(opt);
            }
            else{
                deployments = data;

                data.forEach(element => {
                    let opt = document.createElement('option');
                    opt.value = element['metadata']['guid'];
                    opt.innerHTML = element['entity']['name'];
                    areaActionSelection.appendChild(opt);
                });
                if (currentValue != null && currentValue !== ""){
                    areaActionSelection.value = currentValue;
                }
            }
        }
    );
}

function get_deployment_object_from_id(deploymentId) {

    let deployment = null;
    deployments.forEach(element => {
        if (element['metadata']['guid'] === deploymentId){
            deployment = element;
        }
    });

    return deployment;
}

function send_request(comment) {
    userData.payload.Customer_Service = comment;

    scoringPayload.deployment = get_deployment_object_from_id(areaActionSelection.value);
    scoringPayload.payload = userData.payload;

    $.ajax({
        method: "POST",
        contentType: "application/json",
        url: "/score",
        data: JSON.stringify(scoringPayload),
        success: function (data) {

            feedbackComment.innerHTML = data['text'];
            if(selectedFace !== null){
                responseFace.src = selectedFace.src;
            }

            questionBox.style.display = "none";
            responseBox.style.display = "block";
        },
        error: function (data) {
            print_error(data['responseText']);
        },
        dataType: "json"
    });
}


function select_happy(element) {
    handleClick(element);
    userData.payload.Satisfaction = 1;
    enable_button();
}

function select_sad(element) {
    handleClick(element);
    userData.payload.Satisfaction = 0;
    enable_button();
}

function deselect_faces() {
    if (selectedFace !== null) {
        selectedFace.src = "/static/images/" + selectedFace.id + ".svg";
        selectedFace = null;
    }
    disable_button();
}

function enable_button() {
    let text = textInput.value;

    if (text.length > 10 && selectedFace !== null) {
        sendButton.disabled = false;
    }
}

function disable_button() {
    sendButton.disabled = true;
}

function print_error(text) {
    errorPanel.innerHTML = String(text);
    errorPanel.style.display = "block";
}

function show_hide_sidebar() {
    if(modelSidebar.style.display === "block"){
        show_hide_model_sidebar();
    }
    if (sidebar.style.display === "none") {
        customerName.innerHTML = userData.username + " " + userData.lastname;
        sidebar.style.display = "block";
    }
    else {
        sidebar.style.display = "none"
    }
}

function show_hide_model_sidebar() {
    if(sidebar.style.display === "block"){
        show_hide_sidebar();
    }
    if (modelSidebar.style.display === "none") {
        get_cars4u_deployments();
        modelSidebar.style.display = "block";
    }
    else {
        modelSidebar.style.display = "none"
    }
}

function update_customer_name() {
    userData.username = firstName.value;
    userData.lastname = secondName.value;
    userData.payload.Gender = genderInput.value;
    userData.payload.Age = ageInput.value;
    userData.payload.Status = statusInput.value;
    userData.payload.Children = childrenInput.value;
    userData.payload.Customer_Status = activeInput.value;
    userData.payload.Car_Owner = carownerInput.value;

    document.getElementById("user-welcome").value = "Welcome, " + firstName.value + "!";
}

function reset_sidebar() {
    firstName.value = userData.username;
    secondName.value = userData.lastname;
    genderInput.value = userData.payload.Gender;
    ageInput.value = userData.payload.Age;
    statusInput.value = userData.payload.Status;
    childrenInput.value = userData.payload.Children;
    activeInput.value = userData.payload.Customer_Status;
    carownerInput.value = userData.payload.Car_Owner;
}

let timeout = null;

textInput.onkeyup = function () {
    clearTimeout(timeout);
    timeout = setTimeout(check_typing, 800);
};

function check_typing() {
    let text = textInput.value;

    if (text.length > 10) {
        enable_button();
    }
    else {
        disable_button();
    }
}