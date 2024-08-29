// Delete Account

let deleteModalNew = new bootstrap.Modal(document.getElementById("deleteModal2"));
let deleteAccount = document.getElementById("delete-account");

deleteAccount.addEventListener("click", (e) => {
  deleteAccount.innerText = "Update"
  deleteModalNew.show();
});