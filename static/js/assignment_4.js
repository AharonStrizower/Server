console.log("fetch example");


function getUsers(id) {
    const idNum = document.getElementById(id).value;
    console.log(idNum);
    fetch(' https://reqres.in/api/users/' + idNum).then(
        response => response.json()
    ).then(
        response_obj => put_users_in_html(response_obj.data)
    ).catch(
        err => console.log(err)
    )

}
function put_users_in_html(response_obj_data) {
    console.log(response_obj_data)
    const curr_main = document.querySelector("main");
    const section = document.createElement('section');
    section.innerHTML = `         
        <img src="${response_obj_data.avatar}" alt="Profile picture"/>
        <div>
            <span> ${response_obj_data.first_name} ${response_obj_data.last_name} </span>
            <br>
            <a href="mailto:${response_obj_data.email}"> send email </a>
        </div> `;
    curr_main.appendChild(section);
}