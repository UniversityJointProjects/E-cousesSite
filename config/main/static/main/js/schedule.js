let count_days = 7;
let count_lines = 6;
let days_offset = 6;

let schedule; // Массив ячеект в таблице
let table; // Таблица
let currentDate; // Текущая дата

let event_create_menu; // Меню создания события
let event_show_menu; // Меню отображения события

let left_header_date; // Левая дата заголовка таблицы
let middle_header_date; // Центральная дата заголовка таблицы
let right_header_date; // Правая дата заголовка таблицы

let months_offset = 0; // Смещение месяца, вызванное нажатием на кнопки
let selected_month; // Выбранный месяц в таблице
let selected_year; // Выбранный год в таблице
let saved_year = -1; // Сохранённый год
let saved_relative_year = -1; // Сохранённый относительный год
let week_offset;
let schedule_events = [];
let active_schedule_event;

let page_month;
let page_year;

let months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];


function mod(a, b)
{
    return a < 0 ? b + a % b : a % b;
}

function rand_color(avg_color)
{
    let max_color = 255;
    let min_r = (avg_color * 3 - 2 * max_color);
    let r = min_r + Math.random() * (max_color - min_r);
    let min_g = avg_color * 3 - max_color - r;
    let g = min_g + Math.random() * (max_color - min_g);
    let b = avg_color * 3 - r - g;
    return [r, g, b];
}

function get_month_days_count(month)
{
    month = mod(month, 12);
    if(month == 0 || month == 2 || month == 4 || month == 6 || month == 7 || month == 9 || month == 11)
        return 31;
    else if(month == 1)
    {
        if(month % 4 == 0 || (month % 100 == 0 && month % 400 == 0))
            return 29; // Високосный
        else
            return 28;
    }
    else
        return 30;
}

function get_month_date(week_id, week_day)
{
    month = 0;
    year = 0
    days_left = week_id * 7 + week_day;
    while(days_left >= 0)
    {
        days_left -= get_month_days_count(month);
        month++;
        if(month / 12 == 1)
            year++;
        month %= 12;
    }
    month--;
    if(month < 0) month = 11;
    day = get_month_days_count(month) + days_left;
    return [day, month, year];
}

function get_week_date(day, month, )
{
    let days_left = 0;
    for(let x = 0; x < month; x++)
        days_left += get_month_days_count(x);
    days_left += day;

    week_id = Math.floor(days_left / count_days);
    week_day = days_left % count_days;

    return [week_day, week_id];
}

function fill_date_input()
{
    let select_day_element = $('#select_day');
    let select_month_element = $('#select_month');
    let select_year_element = $('#select_year');
    let select_hour_element = $('#select_hour');
    let select_minute_element = $('#select_minute');

    for(let x = 0; x < 31; x++)
        select_day_element.append($('<option value="' + (x + 1) + '">' + (x + 1) + '</option>'));

    for(let x = 0; x < 12; x++)
        select_month_element.append($('<option value="' + (x + 1) + '">' + months[x] + '</option>'));

    for(let x = 2000; x <= 2050; x++)
        select_year_element.append($('<option value="' + (x - 1999) + '">' + x + '</option>'));

    for(let x = 0; x < 24; x++)
        select_hour_element.append($('<option value="' + (x + 1) + '">' + String(x).padStart(2, '0') + '</option>'));

    for(let x = 0; x < 60; x++)
        select_minute_element.append($('<option value="' + (x + 1) + '">' + String(x).padStart(2, '0') + '</option>'));
}

function on_close_event_menu()
{
    let name_element = $('#id_name');

    let select_day_element = $('#select_day');
    let select_month_element = $('#select_month');
    let select_year_element = $('#select_year');
    let select_hour_element = $('#select_hour');
    let select_minute_element = $('#select_minute');

    let color_element = $('#id_color');
    let description_element = $('#id_description');

    let event_data = {

    };

    $.ajax({
        url: "http://127.0.0.1:8000/schedule/create_event",         /* Куда отправить запрос */
        method: 'post',             /* Метод запроса (post или get) */
        dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
        data: {csrfmiddlewaretoken: window.CSRF_TOKEN,
                                    'name': name_element.val(),
                                    'select_day': select_day_element.val(),
                                    'select_month': select_month_element.val() - 1,
                                    'select_year': (Number(select_year_element.val()) + 1999),
                                    'select_hour': select_hour_element.val(),
                                    'select_minute': select_minute_element.val(),
                                    'color': color_element.val(),
                                    'description': description_element.val()},     /* Данные передаваемые в массиве */
        success: function(data){
              schedule_events = []
              add_to_events(selected_month - 1, selected_year)
              add_to_events(selected_month, selected_year)
              add_to_events(selected_month + 1, selected_year)
        },
        error: function (request, status, error) {
             alert(error);
        }
    });

    event_create_menu.prop('hidden', true);

    update_create_events_menu();
}

class ScheduleEvent
{
    constructor(name, minute, hour, day, month, year, color, description, schedule)
    {
        this.name = name;

        this.minute = minute;
        this.hour = hour;
        this.day = day;
        this.month = month;
        this.year = year;

        this.color = color;
        this.description = description;
        this.schedule = schedule;
    }
}

function update_create_events_menu()
{
    $('#select_day option:selected').each(function(){this.selected=false;});
    $('#select_month option:selected').each(function(){this.selected=false;});
    $('#select_year option:selected').each(function(){this.selected=false;});
    $('#select_hour option:selected').each(function(){this.selected=false;});
    $('#select_minute option:selected').each(function(){this.selected=false;});

    $('#id_name').attr('value', '');
    $('#id_color').attr('value', '');
    $('#id_description').text('');
}

function add_to_events(month, year)
{
    $.ajax({
        url: 'http://127.0.0.1:8000/schedule/get_events',
        method: 'post',
        dataType: 'json',
        data: {csrfmiddlewaretoken: window.CSRF_TOKEN, 'month': mod(month, 12), 'year': year},
        success: function(data) {
            if(data.count_events > 0)
            {
                let lines = data.data.split('\n')
                for(let x = 0; x < lines.length; x++)
                {
                    values = lines[x].split(', ');
                    schedule_events.push(new ScheduleEvent(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], null));
                }
            }
            update_schedule();
        },
        error: function(request, status, error) {

        }
    });
}

function on_click_edit()
{
    event_show_menu.prop('hidden', true);
    event_create_menu.prop('hidden', false);

    let select_day_element = $('#select_day option[value="' + Number(active_schedule_event.day) + '"]');
    let select_month_element = $('#select_month option[value="' + Number(active_schedule_event.month) + '"]');
    let select_year_element = $('#select_year option[value="' + (Number(active_schedule_event.year) - 1999) + '"]');
    let select_hour_element = $('#select_hour option[value="' + (Number(active_schedule_event.hour) + 1) + '"]');
    let select_minute_element = $('#select_minute option[value="' + (Number(active_schedule_event.minute) + 1) + '"]');

    select_day_element.prop('selected', true);
    select_month_element.prop('selected', true);
    select_year_element.prop('selected', true);
    select_hour_element.prop('selected', true);
    select_minute_element.prop('selected', true);

    $('#id_name').attr('value', active_schedule_event.name);
    $('#id_color').attr('value', active_schedule_event.color);
    $('#id_description').text(active_schedule_event.description);
}

function on_click_delete()
{
    event_show_menu.prop('hidden', true);

    $.ajax({
    url: "http://127.0.0.1:8000/schedule/delete_event",
    method: 'post',
    dataType: 'json',
    data: {csrfmiddlewaretoken: window.CSRF_TOKEN, 'day': active_schedule_event.day,
                                                   'month': active_schedule_event.month,
                                                   'year': active_schedule_event.year},
    success: function(data) {

    },
    error: function(request, status, error) {

    }
    });

    window.location.replace('http://127.0.0.1:8000/schedule/' + page_month + '/' + page_year);
}

function get_ellipsis(str, count_symbols)
{
    return str.substr(0, count_symbols) + '...'
}

function update_schedule()
{
      selected_year = currentDate.getFullYear();
      selected_month = currentDate.getMonth();


      let selected_date_in_months = selected_year * 12 + selected_month + months_offset;
      if(saved_year == -1)
      {
            saved_year = selected_date_in_months;
            saved_relative_year = selected_date_in_months % 12;
      }

      //Заполнение данных в header
      left_header_date.text(months[(selected_date_in_months - 1) % 12] + ' ' + Math.floor((selected_date_in_months - 1) / 12));
      middle_header_date.text(months[(selected_date_in_months) % 12] + ' ' + Math.floor(selected_date_in_months / 12));
      right_header_date.text(months[(selected_date_in_months + 1) % 12] + ' ' + Math.floor((selected_date_in_months + 1) / 12));

      week_day_pair = get_week_date(days_offset, selected_date_in_months);
      week_offset = week_day_pair[1];

      for(let x = 0; x < count_days; x++)
        for(let y = 0; y < count_lines; y++)
        {
            schedule[x][y].off('click');
            schedule[x][y].click(function() {

                event_create_menu.prop('hidden', false);

                let date = get_month_date(y + week_offset, x - days_offset);

                let hours = currentDate.getHours();
                let minutes = currentDate.getMinutes();

                let select_day_element = $('#select_day option[value="' + (date[0] + 1) + '"]');
                let select_month_element = $('#select_month option[value="' + (date[1] + 1) + '"]');
                let select_year_element = $('#select_year option[value="' + (Math.floor(selected_date_in_months / 12) - 1999) + '"]');
                let select_hour_element = $('#select_hour option[value="' + (hours + 1) + '"]');
                let select_minute_element = $('#select_minute option[value="' + (minutes + 1) + '"]');

                select_day_element.prop('selected', true);
                select_month_element.prop('selected', true);
                select_year_element.prop('selected', true);
                select_hour_element.prop('selected', true);
                select_minute_element.prop('selected', true);
            });
        }

      //Заполнение таблицы датами
      for(let x = 0; x < count_days; x++)
        for(let y = 0; y < count_lines; y++)
        {
            let date = get_month_date(y + week_offset, x - days_offset);
            let week_day_pair_local = get_week_date(date[0], date[1]);
            schedule[x][y].children('.table_data_cell_left_top').children('.table_data_event').empty();
            schedule[x][y].removeClass('table_data_default_color');
            schedule[x][y].removeClass('table_data_blue_color');
            schedule[x][y].addClass('table_data_default_color');

            schedule[x][y].children('.table_data_cell_left_top').children('.table_data_left_top_number').text(date[0] + 1);
            if(date[1] == selected_date_in_months % 12)
                schedule[x][y].css('color', 'white');
            else
                schedule[x][y].css('color', 'rgba(255, 255, 255, 0.2)');

            for(let i = 0; i < schedule_events.length; i++)
            {
                if(schedule_events[i].day == date[0] + 1 && schedule_events[i].month == date[1] && schedule_events[i].year == date[2])
                {
                    let table_data_event = schedule[x][y].children('.table_data_cell_left_top').children('.table_data_event');
                    table_data_event.append($('<i class="bi bi-calendar-event"></i>'));
                    table_data_event.append($('<a class="event_ref">&nbsp ' + get_ellipsis(schedule_events[i].name, 4) + '</a>').css('color', schedule_events[i].color));
                    schedule_events[i].schedule = schedule[x][y];
                    schedule[x][y].off('click');
                    schedule[x][y].click(function() {
                        event_show_menu.prop('hidden', false);
                        active_schedule_event = schedule_events[i];

                        $('#event_name').text(schedule_events[i].name);
                        $('#event_show_time').text(schedule_events[i].day + ' ' +
                                                   months[schedule_events[i].month - 1] + ' ' +
                                                   schedule_events[i].year + ', ' +
                                                   schedule_events[i].hour + ':' +
                                                   schedule_events[i].minute);
                    });
                }
            }

            if(date[0] + 1 == currentDate.getDate() && date[1] == currentDate.getMonth() && Math.floor(selected_date_in_months / 12) == currentDate.getFullYear())
            {
                schedule[x][y].removeClass('table_data_default_color');
                schedule[x][y].removeClass('table_data_blue_color');
                schedule[x][y].addClass('table_data_blue_color');
            }
        }
}

$(document).ready(function(){
    currentDate = new Date();
    table = $('#table');
    left_header_date = $('#schedule_left_date');
    middle_header_date = $('#schedule_header_date');
    right_header_date = $('#schedule_right_date');

    page_month = $('#event_menu_data').attr('month');
    page_year = $('#event_menu_data').attr('year');

    fill_date_input();

    selected_year = page_year == 0 ? currentDate.getFullYear() : page_year;
    selected_month = page_month == 0 ? currentDate.getMonth() : page_month;
    let selected_date_in_months = selected_year * 12 + selected_month + months_offset;

    let week_day_pair = get_week_date(days_offset, selected_date_in_months);
    week_offset = week_day_pair[1];

    event_create_menu = $('#event_create_menu');
    event_show_menu = $('#event_show_menu');
    schedule = new Array(count_days);
    for(let x = 0; x < count_days; x++)
    {
        schedule[x] = new Array(count_lines);
        for(let y = 0; y < count_lines; y++)
        {
            schedule[x][y] = $('<td class="table_data data_table_schedule__table_data table_data_default_color"><div class="table_data_cell_left_top"></div></td>');
            schedule[x][y].children('.table_data_cell_left_top').append($('<div class="table_data_left_top_number"></div>'));
            schedule[x][y].children('.table_data_cell_left_top').append($('<div class="table_data_event"></div>'));
            schedule[x][y].click(function() {

                event_create_menu.prop('hidden', false);

                let date = get_month_date(y + week_offset, x - days_offset);

                let hours = currentDate.getHours();
                let minutes = currentDate.getMinutes();

                let select_day_element = $('#select_day option[value="' + (date[0] + 1) + '"]');
                let select_month_element = $('#select_month option[value="' + (date[1] + 1) + '"]');
                let select_year_element = $('#select_year option[value="' + (Math.floor(selected_date_in_months / 12) - 1999) + '"]');
                let select_hour_element = $('#select_hour option[value="' + (hours + 1) + '"]');
                let select_minute_element = $('#select_minute option[value="' + (minutes + 1) + '"]');

                select_day_element.prop('selected', true);
                select_month_element.prop('selected', true);
                select_year_element.prop('selected', true);
                select_hour_element.prop('selected', true);
                select_minute_element.prop('selected', true);
            });
        }
    }

    $('#id_event_menu_cross').click(function() {
        event_create_menu.prop('hidden', true);
        update_create_events_menu();
    });

    $('#id_show_event_menu_cross').click(function() {
        event_show_menu.prop('hidden', true);
        update_create_events_menu();
    });

    for(let y = 0; y < count_lines; y++)
    {
        row = $('<tr></tr>')
        for(let x = 0; x < count_days; x++)
            row.append(schedule[x][y]);
        table.append(row);
    }

      // Добавление событий
      schedule_events = []
      add_to_events(selected_month - 1, selected_year)
      add_to_events(selected_month, selected_year)
      add_to_events(selected_month + 1, selected_year)

    left_header_date.click(function(){
        months_offset--;
        schedule_events = []
        add_to_events(selected_month - 1, selected_year)
        add_to_events(selected_month, selected_year)
        add_to_events(selected_month + 1, selected_year)
        update_schedule();
    });

    right_header_date.click(function(){
        months_offset++;
      schedule_events = []
        add_to_events(selected_month - 1, selected_year)
        add_to_events(selected_month, selected_year)
        add_to_events(selected_month + 1, selected_year)
        update_schedule();
    });
});