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


/* Remove path */
function path_remove(node_id) {

    event.preventDefault();
    event.stopPropagation();

    let data = new FormData();
    data.append('node_id', node_id);

    zajaxPost(path_remove_url, data, path_remove_assert, ack, false);
}


/* Assert remove path */
async function path_remove_assert(reply_json) {

    let data = JSON.parse(reply_json);

    let node = document.getElementById('path_card_' + data.node_id);
    node.remove();
}


/* Move path */
function path_move(operation, node_id) {

    event.preventDefault();
    event.stopPropagation();

    let data = new FormData();
    data.append('operation_id', operation);
    data.append('node_id', node_id);

    zajaxPost(path_move_url, data, path_move_assert, ack, false);
}


/* Assert remove path */
async function path_move_assert(reply_json) {

    let data = JSON.parse(reply_json);

    let parent_node = document.getElementById('path_content_' + data.parent_id);
    // let previous_node = document.getElementById('path_card_' + data.previous_id);
    let next_node = document.getElementById('path_card_' + data.next_id);
    // let next_content = document.getElementById('path_content_' + data.next_id);
    let node = document.getElementById('path_card_' + data.node_id);

    // if (data.operation_id == 'parent') {

    //     if (parent_node) {
    //         parent_node.insertBefore(node, next_node);
    //     }

    // } else if (data.operation_id == 'child') {

    //     if (parent_node) {
    //         parent_node.insertBefore(node, next_node);
    //     }
    // } else if (data.operation_id == 'previous') {

    //     if (parent_node) {
    //         parent_node.insertBefore(node, next_node);
    //     }
    // } else if (data.operation_id == 'next') {

    //     if (parent_node) {
    //         parent_node.insertBefore(node, next_node);
    //     }
    // }

    if (parent_node) {
        parent_node.insertBefore(node, next_node);
    }
}


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

document.querySelectorAll('.dummy').forEach(item => {
    item.addEventListener('click', event => {

        let lst = document.getElementsByClassName("dummy active");
        var i;
        for (el of lst) {
            el.classList.remove("active");
        }

        console.log(item);
        lst = item.classList;
        console.log(lst);
        lst = item.classList.toggle("active");
    })
})


function content_add(element, root_path_id, source_id, content_id) {

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

    data.append('root_path_id', root_path_id);

    let lst = document.getElementsByClassName("dummy active");
    console.log(lst)
    if (lst.length) {
        // path_id = lst[0].getAttribute("data-target")
        path_id = lst[0].getAttribute("data-target")
    } else {
        path_id = 0
    }
    data.append('path_id', path_id);

    data.append('source_id', source_id);
    data.append('content_id', content_id);

    zajaxPost(parse_content_add_url, data, content_add_assert, ack, false);
}


/* Assert favorite setting */
async function content_add_assert(reply_json) {

    let data = JSON.parse(reply_json);

    if ('path_id' in data) {

        /* Toggle image state */
        let element = document.getElementById("subs_" + data.ytb_channel_id);
        let img = element.children;

        im_type = img[0].getAttribute('data-prefix');
        if (im_type == 'far') {
            img[0].setAttribute('data-prefix', 'fas');
        } else {
            img[0].setAttribute('data-prefix', 'far');
        }
    }
}