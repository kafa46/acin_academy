/* Progress-bar 컨트롤 
    Created by ACIN Academy
    Written by Prof. Giseop Noh
*/

// 테스트 코드
// $(function () {
//     update_progressbar(95)
// })


// Progressbar 업데이트 함수
function update_progressbar(percent) {
    let p_bar = $('#p_bar');
    p_bar.css('width', `${percent}%`);
    p_bar.attr('aria-valuenow', percent);
    p_bar.text(`${percent}%`);
}


// socket.io 구현
$(function(){
    const socket = io();
    let socket_id = undefined;
    socket.connect(`http://192.168.0.16:5678`, function(){
        socket_id = socket.id;
        console.log('success');
    });
    // socket.on('connect', function(){
    //     console.log('success');
    // });
    const result_text_area=  $('#result_text_area');
    result_text_area.attr('hidden', true);
    socket.on('process_status', function(percent){
        const p_bar_area = $('#p_bar_area');
        if (percent < 100){
            p_bar_area.attr('hidden', false);
            console.log(`Progress: ${percent}%`);
            update_progressbar(percent);
        } else {
            update_progressbar(0);
            p_bar_area.attr('hidden', true);
            result_text_area.attr('hidden', false);
        }
    });
});
