
$(document).ready(function(){
    let user_id = $('.progress_help_div').attr('user_id');
    let course_id = $('.progress_help_div').attr('course_id');

    passed_content = 'Пройдено';
    not_passed_content = 'Отметить как пройдено';

    $('.progress_button').each(function(){
        let obj = $(this)
        let button_id = $(this).attr('button_id');
        $.ajax({
        url: 'http://127.0.0.1:8000/course/get_progress_state',
        method: 'post',
        dataType: 'json',
        data: {csrfmiddlewaretoken: window.CSRF_TOKEN,  'button_id': button_id,
                                                        'user_id': user_id,
                                                        'course_id': course_id},
        success: function(data) {
            if (data.state)
            {
                if (obj.hasClass('progress_button_deactivated'))
                    obj.removeClass('progress_button_deactivated');
                obj.addClass("progress_button_activated");
                obj.text(passed_content)
            }
            else
            {
                if (obj.hasClass('progress_button_activated'))
                    obj.removeClass('progress_button_activated');
                obj.addClass("progress_button_deactivated");
                obj.text(not_passed_content)
            }
        },
        error: function(request, status, error) {
        }});
    });

    $('.progress_button').click(function(){
        let button_id = $(this).attr('button_id');
        obj = $(this)
        $.ajax({
            url: 'http://127.0.0.1:8000/course/switch_progress_state',
            method: 'post',
            dataType: 'json',
            data: {csrfmiddlewaretoken: window.CSRF_TOKEN,  'button_id': button_id,
                                                            'user_id': user_id,
                                                            'course_id': course_id},
            success: function(data) {
                if (data.state)
                {
                    if (obj.hasClass('progress_button_deactivated'))
                        obj.removeClass('progress_button_deactivated');
                    obj.addClass("progress_button_activated");
                    obj.text(passed_content)
                }
                else
                {
                    if (obj.hasClass('progress_button_activated'))
                        obj.removeClass('progress_button_activated');
                    obj.addClass("progress_button_deactivated");
                    obj.text(not_passed_content)
                }
            },
            error: function(request, status, error) {
        }});
    });
});