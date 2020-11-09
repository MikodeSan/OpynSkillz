// /* Add sub-path */
// function add_sub_path(path_id, parent_id) {

//     event.preventDefault();
//     event.stopPropagation();

//     let data = new FormData();
//     data.append('root_path_id', path_id);
//     data.append('parent_path_id', parent_id);

//     zajaxPost(parse_add_path_url, data, add_sub_path_assert, ack, false);
// }


// /* Assert favorite setting */
// async function add_sub_path_assert(reply_json) {

//     let data = JSON.parse(reply_json);
//     // console.log(typeof data.code);
//     console.log(data);
// }


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


function subscribe(element, path_id, channel_id) {

    event.preventDefault();
    event.stopPropagation();

    let img = element.children;
    im_type = img[0].getAttribute('data-prefix');

    let data = new FormData();
    if (im_type == 'far') {
        data.append('enable', true);
    } else {
        data.append('enable', false);
    }
    data.append('path_id', path_id);
    data.append('channel_id', channel_id);

    zajaxPost(parse_channel_subcription_url, data, subscribe_assert, ack, false);
}


/* Assert favorite setting */
async function subscribe_assert(reply_json) {

    let data = JSON.parse(reply_json);

    if ('path_id' in data) {

        /* Toggle image state */
        let element = document.getElementById("subs_" + data.ytb_channel_id);
        let img = element.children;

        // img[0].classList.toggle("fa-thumbs-down");
        // img[0].classList.toggle("fa-thumbs-up");

        im_type = img[0].getAttribute('data-prefix');
        if (im_type == 'far') {
            img[0].setAttribute('data-prefix', 'fas');
        } else {
            img[0].setAttribute('data-prefix', 'far');
        }
    }
}