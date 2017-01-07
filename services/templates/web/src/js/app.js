var apiURL = "/api";

$(document).ready(function() {
    //prevent zooming
    interact('body')
        .on('doubletap', function(ev) {
            ev.preventDefault();
        });

    //prevent pinch to zoom
    interact('body')
        .gesturable({
            onstart: function(ev) {
                ev.preventDefault();
            }
        });


});
$(document).delegate('.error-whole-number', 'keyup', function(ev) {
    $(this).removeClass('error-whole-number');
});
//Added this to Remove the Error Handling in Settings Unit Cost Page.
$(document).delegate('.has-error', 'blur', function(ev) {
    $(this).removeClass('has-error');
    $(this).parent().removeClass('has-error');
    $(this).parent().find('.help-block').remove();
    $(this).parent().parent().removeClass('has-error');
    $(this).parent().parent().find('.help-block').remove();
});
$(document).delegate('.panel-heading', 'click', function(ev) {
    $('.panel-collapse').removeClass('in');
    //$(this).next().addClass('in');
});

// $(document).delegate('.date-pick','dp.show',function(ev){
//   $('.picker-switch').css('pointer-events','none');
// });

Handlebars.registerHelper('equaltoo', function(lvalue, rvalue, options) {
    if (arguments.length < 3)
        throw new Error('Handlebars Helper equal needs 2 parameters')
    if (lvalue === rvalue) {
        return options.fn(this)
    } else {
        return options.inverse(this)
    }
});

Handlebars.registerHelper('slugify', function(options) {
    return options.fn(this)
        .toLowerCase()
        .replace(/ /g, '-')
        .replace(/[^\w-]+/g, '');
});

Handlebars.registerHelper('thresholdhighlight', function(options) {
    var value = options.fn(this);
    var originalValue = value.split('-')[0];
    var thresholValue = value.split('-')[1];
    if (parseInt(originalValue) > parseInt(thresholValue)) {
        return 'color:red;';
    } else {
        return '';
    }
});

Handlebars.registerHelper('textQuestion', function(questionInfo, question, options) {
    //var value=options.fn(this);
    //var dataQuestion=$('[data-questionId|="'+value+'"]').data();
    //var value=dataQuestion.questionInfo?dataQuestion.questionInfo:'';
    if (question.indexOf("#text#") != -1) {
        var newQuestion = "<input class='js-question-extra-info' type='text' value='" + questionInfo + "'></input>";
        var returnQuestion = question.replace('#text#', newQuestion);
    } else {
        var returnQuestion = question;
    }
    return returnQuestion;
});

Handlebars.registerHelper('completedQuestion', function(questionInfo, question, options) {
    if (question.indexOf("#text#") != -1) {
        var returnQuestion = question.replace('#text#', questionInfo);
    } else {
        var returnQuestion = question;
    }
    return returnQuestion;
});



Handlebars.registerHelper('datetostring', function(options) {
    return moment(options.fn(this)).format('MMM Do YYYY');
});
Handlebars.registerHelper('trimtime', function(options) {
    if (options.fn(this)) {
        return options.fn(this).substring(0, 5);
    } else {
        return '';
    }
});

Handlebars.registerHelper('statusdisplay', function(options) {
    if (options.fn(this) && options.fn(this) == 'completed') {
        return 'Completed';
    } else {
        return 'Saved';
    }
});

Handlebars.registerHelper('storeProfileExist', function(profileList, key, options) {
    var returnFlag = false;
    for (var i = 0; i < profileList.length; i++) {
        if (profileList[i].profile_code === key) {
            returnFlag = true;
            break;
        }
    }
    if (returnFlag) {
        return options.fn(this);
    } else {
        return options.inverse(this);
    }
});

Handlebars.registerHelper('topoint', function(options) {
    if (options.fn(this)) {
        var s = options.fn(this);
        return new Number(s).toString();
    } else {
        return '';
    }

});

Handlebars.registerHelper('ifCond', function(v1, v2, options) {
    if (v1 === v2) {
        return options.fn(this);
    }
    return options.inverse(this);
});


Handlebars.registerHelper('arrayLength', function(v1, v2, options) {
    if (v1 > v2) {
        return options.fn(this);
    }
    return options.inverse(this);
});

Handlebars.registerHelper('eachItem', function(context, options) {
    var ret = "";
    for (var i = 0, j = 5; i < j; i++) {
        ret = ret + options.fn(context[i]);
    }
    return ret;
});

Handlebars.registerHelper('eachArray', function(context, options) {
    var ret = 0;
    for (var i = 0, j = context.length; i < j; i++) {
        if (context[i].pull_value != null) {
            ret = ret + context[i].pull_value;
        }
    }
    return ret;
});

Handlebars.registerHelper('getTheWeek', function(options) {
    return moment(options).format('dddd');
});

Handlebars.registerHelper('verify', function(options) {
    var slotsArray = [{
        time_range: "9pm-10pm"
    }, {
        time_range: "10pm-11pm"
    }, {
        time_range: "11pm-00am"
    }, {
        time_range: "00am-1am"
    }];
    if (options == "00am-1am") {
        return "<div class='js-header_slot'>9pm-10pm</div>";
    } else if (options == "9pm-10pm") {
      return "<small class='js-header_slot1'>10pm-11pm</small>";
    } else if (options == "10pm-11pm") {
      return "<small class='js-header_slot1'>11pm-00am</small>";
    } else if (options == "11pm-00am") {
      return "<div class='js-header_slot'>00am-1am</div>";
    } else {
        return options;
    }
});
