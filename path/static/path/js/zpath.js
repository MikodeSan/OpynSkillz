/* Set favorite state for the specified product */
function search_source() {

    event.preventDefault();
    event.stopPropagation();

    let query_in = document.getElementById('sandbox_search_id');

    let data = new FormData();
    data.append('query', query_in.value);
    // data.append('favorite', flag);

    zajaxPost(parse_source_query_url, data, search_source_assert, ack, false);
}


/* Assert favorite setting */
async function search_source_assert(reply_json) {

    let data = JSON.parse(reply_json);
    // console.log(typeof data.code);
    console.log(data);

    /* Change favorite image state and callback flag */
    // let cur_a = document.getElementById(data.code);

    /* [TODO]: DRY to optimize */

    // if (data.favorite) {
    //     image_type = 'far';
    // } else {
    //     image_type = 'fas';
    // }

    // cur_a.innerHTML = "<i class='" + image_type + " fa-1x fa-heart mb-4'></i>";

    // let s = arguments.callee.name + '(' + data.code + ', ' + data.favorite + ')';
    // cur_a.setAttribute('data-state', data.favorite);
}

/* test */
const ack = () => {

    // console.log('Favorite setting Ack !');
    // console.log('function name:' + arguments.callee.name);
};