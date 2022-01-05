async function postData(url = '', data = {}, method='POST') {
    // Default options are marked with *
    const response = await fetch(url, {
        method: method, // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}
    const delBtns = document.getElementsByClassName("delBtn");
    for(let i=0; i< delBtns.length; i++)
    {
        delBtns[i].addEventListener('click', function(){
            postData('books', { id: this.getAttribute('data-id'), action: 'delete_book' }, 'DELETE')
            .then(data => {
                console.log(data)
                if(data['result'] == 'fail') {
                    alert('Oops! The books has relation with authors/categories, please delete the relation at first.');
                } else {
                    alert('The books has been deleted.');
                }
                location.reload();
            });
        })
    }


function closeEditModal()
{
    editModal.classList.add('fade');
    editModal.setAttribute('aria-hidden',true);
    editModal.style.display = 'none';
}

const editBtns = document.getElementsByClassName("editBtn");
const editModal = document.getElementById("editModal");
const editModalClose1 = document.getElementById('editModalClose1');
const editModalClose2 = document.getElementById('editModalClose2');
const isbn_input = document.getElementById('edit_isbn');
const publisher_input = document.getElementById('edit_publisher');
const title_input = document.getElementById('edit_title');
const year_input = document.getElementById('edit_year');
const IdInput = document.getElementById('bookId');

editModalClose1.addEventListener('click',closeEditModal);
editModalClose2.addEventListener('click',closeEditModal);

for(let i=0; i< editBtns.length; i++)
{
    editBtns[i].addEventListener('click', function(){
        let Id = this.getAttribute('data-id');
        let isbn = this.getAttribute('data-isbn');
        let publisher = this.getAttribute('data-publisher');
        let title = this.getAttribute('data-title');
        let year = this.getAttribute('data-year');

        isbn_input.value = isbn;
        publisher_input.value = publisher;
        title_input.value = title;
        year_input.value = year;
        IdInput.value = Id;
        editModal.classList.remove('fade');
        editModal.setAttribute('aria-hidden',false);
        editModal.style.display = 'block';
    })
}