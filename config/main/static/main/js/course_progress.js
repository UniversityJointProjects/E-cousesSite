
$(document).ready(function(){
    let user_id = $('.progress_help_div').attr('user_id');
    let course_id = $('.progress_help_div').attr('course_id');

    $('.pass_button').click(function(){
        let state = false;
        if ($(this).children().hasClass('mark_as_passed'))
        {
            $(this).children().removeClass('mark_as_passed');
            $(this).children().addClass('passed');
            state = true;
        }
        else {
            $(this).children().removeClass('passed');
            $(this).children().addClass('mark_as_passed');
            state = false;
        }
        let button_id = $(this).attr('button_id');
        $.ajax({
            url: 'http://127.0.0.1:8000/course/save_progress',
            method: 'post',
            dataType: 'json',
            data: {csrfmiddlewaretoken: window.CSRF_TOKEN,  'button_id': button_id,
                                                            'user_id': user_id,
                                                            'course_id': course_id,
                                                            'state': state},
            success: function(data) {},
            error: function(request, status, error) {
            }});
    });





//    $('.pass_button').click(function(){
//        let state = false;
//        if ($(this).children().hasClass('mark_as_passed'))
//        {
//            $(this).children().removeClass('mark_as_passed');
//            $(this).children().addClass('passed');
//            state = true;
//        }
//        else {
//            $(this).children().removeClass('passed');
//            $(this).children().addClass('mark_as_passed');
//            state = false;
//        }
//        let button_id = $(this).attr('button_id');
//        $.ajax({
//            url: 'http://127.0.0.1:8000/course/save_progress',
//            method: 'post',
//            dataType: 'json',
//            data: {csrfmiddlewaretoken: window.CSRF_TOKEN,  'button_id': button_id,
//                                                            'user_id': user_id,
//                                                            'course_id': course_id,
//                                                            'state': state},
//            success: function(data) {},
//            error: function(request, status, error) {
//            }});
//    });
});