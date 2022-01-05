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
            postData('booksCategories', { id_1: this.getAttribute('data-id-1'), id_2: this.getAttribute('data-id-2'), action: 'delete_book_category' }, 'DELETE')
            .then(data => {
                console.log(data)
                alert('The Relationship has been deleted.');
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
const category_id_input = document.getElementById('categoryId_bc');
const category_id_old = document.getElementById('category_id_old');
const book_id_input = document.getElementById('bookId_bc');

editModalClose1.addEventListener('click',closeEditModal);
editModalClose2.addEventListener('click',closeEditModal);

for(let i=0; i< editBtns.length; i++)
{
    editBtns[i].addEventListener('click', function(){
        let bookId = this.getAttribute('data-id-1');
        let categoryId = this.getAttribute('data-id-2');

        category_id_input.value = categoryId;
        category_id_old.value = categoryId;
        book_id_input.value = bookId;
        editModal.classList.remove('fade');
        editModal.setAttribute('aria-hidden',false);
        editModal.style.display = 'block';
    })
}