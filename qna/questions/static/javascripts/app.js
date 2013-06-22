;(function ($, window, undefined) {
  'use strict';

  var $doc = $(document),
      Modernizr = window.Modernizr;

  $(document).ready(function() {
    $.fn.foundationAlerts           ? $doc.foundationAlerts() : null;
    $.fn.foundationButtons          ? $doc.foundationButtons() : null;
    $.fn.foundationAccordion        ? $doc.foundationAccordion() : null;
    $.fn.foundationNavigation       ? $doc.foundationNavigation() : null;
    $.fn.foundationTopBar           ? $doc.foundationTopBar() : null;
    $.fn.foundationCustomForms      ? $doc.foundationCustomForms() : null;
    $.fn.foundationMediaQueryViewer ? $doc.foundationMediaQueryViewer() : null;
    $.fn.foundationTabs             ? $doc.foundationTabs({callback : $.foundation.customForms.appendCustomMarkup}) : null;
    $.fn.foundationTooltips         ? $doc.foundationTooltips() : null;
    $.fn.foundationMagellan         ? $doc.foundationMagellan() : null;
    $.fn.foundationClearing         ? $doc.foundationClearing() : null;

    $.fn.placeholder                ? $('input, textarea').placeholder() : null;
  });

  // UNCOMMENT THE LINE YOU WANT BELOW IF YOU WANT IE8 SUPPORT AND ARE USING .block-grids
  // $('.block-grid.two-up>li:nth-child(2n+1)').css({clear: 'both'});
  // $('.block-grid.three-up>li:nth-child(3n+1)').css({clear: 'both'});
  // $('.block-grid.four-up>li:nth-child(4n+1)').css({clear: 'both'});
  // $('.block-grid.five-up>li:nth-child(5n+1)').css({clear: 'both'});

  // Hide address bar on mobile devices (except if #hash present, so we don't mess up deep linking).
  if (Modernizr.touch && !window.location.hash) {
    $(window).load(function () {
      setTimeout(function () {
        window.scrollTo(0, 1);
      }, 0);
    });
  }

})(jQuery, this);

// Controls what happens when you click on an answer.

$(document).ready(function(){
  $('.answer').click(function(e) {
    e.preventDefault();
    $('#previous_question, #current_question').fadeOut(300);
      $.ajax({
        url: '/questions/' + this.id + '/vote' + '/',
        success: function(data) {
            $('#current_question').html('&nbsp;').load("/questions/"+data.current_question_pk +"/").hide().fadeIn(300);
            $('#previous_question').html('&nbsp;').load('/questions/previous_question/' + data.previous_question_pk + "/").hide().fadeIn(400);
        }
      });
  });
});

// Controls addition of new boxes to submit form.

$(document).ready(function() {
  // Code adapted from http://djangosnippets.org/snippets/1389/
  function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+-)');
    var replacement = prefix + '-' + ndx + '-';
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
 replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
  }

  function deleteForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

    if (formCount > 1) {
      // Delete the item/form
      $(btn).parents('.answer').remove();

      var forms = $('.answer'); // Get all the forms

      // Update the total number of forms (1 less than before)
      $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);

      var i = 0;
      // Go through the forms and set their indices, names and IDs
      for (formCount = forms.length; i < formCount; i++) {
        $(forms.get(i)).children().children().each(function() {
          updateElementIndex(this, prefix, i);
        });
      }

    } // End if
    else {
        alert("You have to enter at least one answer!");
    }
    return false;
  }

  function addForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

    // You can only submit a maximum of 10 todo items
    if (formCount < 5) {
      // Clone a form (without event handlers) from the first form
      var row = $(".answer:first").clone(false).get(0);
      // Insert it after the last form
      $(row).removeAttr('id').hide().insertAfter(".answer:last").slideDown(300);

      // Remove the bits we don't want in the new row/form
      // e.g. error messages
      $(".errorlist", row).remove();
      $(row).children().removeClass('error');

      // Relabel/rename all the relevant bits
      $(row).children().children().each(function() {
        updateElementIndex(this, prefix, formCount);
        if ( $(this).attr('type') == 'text' )
          $(this).val('');
      });

      // Add an event handler for the delete item/form link
      $(row).find('.delete').click(function() {
        return deleteForm(this, prefix);
      });

      // Update the total form count
      $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);

    } // End if
    else {
      alert("Sorry, you can only enter a maximum of five items.");
    }
    return false;
  }

  // Register the click event handlers
  $("#add").click(function() {
    return addForm(this, 'form');
  });

  $(".delete").click(function() {
    return deleteForm(this, 'form');
  });
});

// Facebook Login and Logout.


  $('.login').click(function(e) {
    e.preventDefault();
    FB.login(function(response) {
      var access_token=response.authResponse.accessToken;
      window.location.href =  '/facebook_login_success?access_token=' + access_token;
}, {scope: 'email,user_birthday,user_education_history,user_hometown,user_location,user_questions,user_relationships,user_religion_politics,user_work_history,user_interests,user_activities'});
  });

  $('.logout').click(function(e){
    e.preventDefault();
    FB.logout(function(response){
      window.location.href = '/logout/';
    });

  });

  $(function() {
// placement examples
  $('.north').powerTip({ placement: 'n' });
  $('.east').powerTip({ placement: 'e' });
  $('.south').powerTip({ placement: 's' });
  $('.west').powerTip({ placement: 'w' });
  $('.north-west').powerTip({ placement: 'nw' });
  $('.north-east').powerTip({ placement: 'ne' });
  $('.south-west').powerTip({ placement: 'sw' });
  $('.south-east').powerTip({ placement: 'se' });
  $('.north-west-alt').powerTip({ placement: 'nw-alt' });
  $('.north-east-alt').powerTip({ placement: 'ne-alt' });
  $('.south-west-alt').powerTip({ placement: 'sw-alt' });
  $('.south-east-alt').powerTip({ placement: 'se-alt' });
});

$(function(){
        $(document).foundation(); 

})