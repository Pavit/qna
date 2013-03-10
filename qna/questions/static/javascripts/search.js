

    $(function() {

      $.ui.autocomplete.prototype._renderItem = function(ul, item) {
        return $("<li></li>").data("item.autocomplete", item).append($("<a></a>").html(item.label)).appendTo(ul);
      };

      $("#search").autocomplete({
        source: function(request, response) {
          var pavdude = request.term;
          $.ajax({
            url: "{% url search %}?searchtext=" + request.term,
            type: "GET",
            success: function(data) {

              response($.map(data, function(item) {
                data.slice(0,6);
                return {
                  label: item.fields.question,
                  value: item.pk
                }
              }));
            },
            data: request.term,
            dataType: "json"
          });
          var searchtext = request.term;
          response(results.slice(0,6));
        },

        response: function(event, ui) {
          ui.content.push({
            label:  "<b>Show All Search Results</b>",
            value: ui
          });
          ui.content.push({
            label:  "<b>Submit New Question</b>",
            value: ui
          });
        },
        select: function(event, ui) {
          event.preventDefault()
          if (ui.item.label == "<b>Show All Search Results</b>")
          {
            var searchtext = $("#search").val();
            $('#previous_question').fadeOut(300);
            $('#current_question').fadeOut(300);
            $('#search_results').html('&nbsp;').load('/search_results/'+searchtext+"/");
          }
          else if (ui.item.label == "<b>Submit New Question</b>")
            {
              $('#previous_question').fadeOut(300);
              $('#current_question').fadeOut(300);
              window.open("/submitquestion/","_self");
            }
          else
          {
            var url = "/current_question/" + ui.item.value;
            $('#previous_question').fadeOut(300);
            $('#current_question').delay(200).fadeOut(300);
            $('#current_question').html('&nbsp;').load(url);
            $('#current_question').fadeIn(300);
            $('#previous_question').fadeIn(300);
          };
        }
      })
    });