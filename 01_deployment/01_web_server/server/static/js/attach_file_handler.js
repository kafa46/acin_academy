/* 첨부 파일 처리 핸들러
    - 참고문서
        1. https://purecho.tistory.com/68
        2. https://codepen.io/green526/embed/qBjZLex?height=537&default-tab=html%2Cresult&slug-hash=qBjZLex&editable=true&user=green526&ke-size=size16&name=cp_embed_1
*/

// csrf_token 초기화
$(function(){
    var csrf_token = $('#csrf_token').val();
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
});

var FILE_NUM = 0; // 첨부된 파일 개수
var FILE_ARRAY = new Array(); // 첨부 파일 저장용 배열

/* 파일 추가 함수 */
function add_file(obj){
    let max_file_count = 10; //첨부파일 최대 개수
    let attach_file_count = $('.filebox').length;
    let remain_file_count = max_file_count - attach_file_count;
    let current_file_count = obj.files.length; // 현재 첨부된 파일 개수
    $('#attached-file-list').attr('hidden', false)
    // 첨부파일 개수 확인
    if (current_file_count > remain_file_count) {
        alert(`첨부파일은 최대 ${max_file_count}개 까지 첨부 가능합니다.`);
    } else {
        for (const file of obj.files) {
            // 첨부파일 검증
            if (validation(file)) {
                // 파일 배열에 담기
                let reader = new FileReader();
                reader.readAsDataURL(file); // 파일 읽기
                reader.onload = function () {
                    FILE_ARRAY.push(file); //읽기 성공 -> 배열에 저장
                };
                // 파일 목록을 화면에 추가
                const img_path = '<img src="/static/imgs/delete-doc.ico" width="20px" alt="문서 삭제">'
                let html_data =`
                <div class="filebox my-2 ml-2" id="file${FILE_NUM}">
                    <p class="name">
                        첨부${FILE_NUM + 1}: ${file.name}
                        <span>
                            <a class="delete" onclick="deleteFile(${FILE_NUM});">${img_path}</a>
                        </span>
                    </p>
                </div>`
                $('.file-list').append(html_data);
                FILE_NUM++;
            } else {
                continue;
            }
        }
    }
    // 첨부 파일을 저장하였으므로 Form input 내용 초기화
    $('input[type=file').val('')
}


/* 파일을 form에 저장  */
function saveFilesToForm(){
    let form = $('form');
    let form_data = new FormData(form[0]);
    for(let i=0; i<FILE_ARRAY.length; i++){
        form_data.append('file', FILE_ARRAY[i])
    }
    return form_data
}


/* 첨부파일 검증 */
function validation(obj){
    const fileTypes = [
        'application/pdf',
        'application/haansofthwp',
        'application/x-hwp',
        'application/msword', // .doc
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // .docx
        'application/vnd.ms-excel', // .xls
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
        'video/x-msvideo', // .avi
        'application/zip',
        'audio/mpeg',
        'video/mp4',
        'video/mpeg',
        'image/gif',
        'image/jpeg',
        'image/png',
        'image/bmp',
        'image/tif',
        'text/plain', // .txt
        'text/csv', // .csv
    ];
    if (obj.name.length > 200) {
        alert("파일명이 200자 이상인 파일은 제외되었습니다.");
        return false;
    } else if (obj.size > (500 * 1024 * 1024)) {
        alert("최대 파일 용량인 500MB를 초과한 파일은 제외되었습니다.");
        return false;
    } else if (obj.name.lastIndexOf('.') == -1) {
        alert("확장자가 없는 파일은 제외되었습니다.");
        return false;
    } else if (!fileTypes.includes(obj.type)) {
        alert("지원하지 않는 파일 형식입니다. 첨부 불가 파일은 제외되었습니다.");
        return false;
    } else {
        return true;
    }
}


/* 첨부파일 삭제 */
function deleteFile(num) {
    document.querySelector("#file" + num).remove();
    FILE_ARRAY.splice(num, 1)
    FILE_NUM--;
}


$(function(){
    /* 서버 전송하기 버튼을 클릭한 경우 서버 전송 처리 */
    let submit_btn = $('#submit_files');
    submit_btn.on('click', function(e){
        // 파일이 첨부되어 있는지 확인
        if(FILE_NUM===0){
            alert('첨부파일이 없습니다.\n분석할 파일을 추가해 주세요');
            return;
        }
        // 분석할 파일이 있다면 서버로 전송
        let form_data = saveFilesToForm();
        e.preventDefault();
        $.ajax({
            method: 'POST',
            url: '/process',
            data: form_data,
            dataType: 'json',
            contentType: false,
            processData: false,
            cache: false,
            success: function(result){
                console.log(result['content'])
                let text_area = $('#floatingTextarea2');
                $('#textarea_label').remove();
                text_area.attr('readonly', false)
                text_area.val(result['content'])
                text_area.attr('readonly', true)

            },
            error: function(error){
                alert('에러가 발생했습니다. 관리자에게 문의해 주세요');
                console.log(error);
                return;
            }
        });
    });

    /* 화면 초기화 버튼을 클릭했을 경우 처리*/
    $('#clear-content-btn').on('click', function(){
        location.reload();
    });

});

