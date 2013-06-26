(function(/*! Brunch !*/) {
  'use strict';

  var globals = typeof window !== 'undefined' ? window : global;
  if (typeof globals.require === 'function') return;

  var modules = {};
  var cache = {};

  var has = function(object, name) {
    return ({}).hasOwnProperty.call(object, name);
  };

  var expand = function(root, name) {
    var results = [], parts, part;
    if (/^\.\.?(\/|$)/.test(name)) {
      parts = [root, name].join('/').split('/');
    } else {
      parts = name.split('/');
    }
    for (var i = 0, length = parts.length; i < length; i++) {
      part = parts[i];
      if (part === '..') {
        results.pop();
      } else if (part !== '.' && part !== '') {
        results.push(part);
      }
    }
    return results.join('/');
  };

  var dirname = function(path) {
    return path.split('/').slice(0, -1).join('/');
  };

  var localRequire = function(path) {
    return function(name) {
      var dir = dirname(path);
      var absolute = expand(dir, name);
      return globals.require(absolute);
    };
  };

  var initModule = function(name, definition) {
    var module = {id: name, exports: {}};
    definition(module.exports, localRequire(name), module);
    var exports = cache[name] = module.exports;
    return exports;
  };

  var require = function(name) {
    var path = expand(name, '.');

    if (has(cache, path)) return cache[path];
    if (has(modules, path)) return initModule(path, modules[path]);

    var dirIndex = expand(path, './index');
    if (has(cache, dirIndex)) return cache[dirIndex];
    if (has(modules, dirIndex)) return initModule(dirIndex, modules[dirIndex]);

    throw new Error('Cannot find module "' + name + '"');
  };

  var define = function(bundle, fn) {
    if (typeof bundle === 'object') {
      for (var key in bundle) {
        if (has(bundle, key)) {
          modules[key] = bundle[key];
        }
      }
    } else {
      modules[bundle] = fn;
    }
  };

  globals.require = require;
  globals.require.define = define;
  globals.require.register = define;
  globals.require.brunch = true;
})();

window.require.register("demo/sunburst", function(exports, require, module) {
  var pollChart, showSunburst;

  require("init");

  pollChart = window.pollChart;

  showSunburst = function(file) {
    d3.select("#sunburst").html("");
    return pollChart.sunburst({
      el: "#sunburst",
      src: file,
      fields: ["gender", "agegroup", "political"],
      labels: ["Gender", "Age Group", "Politics"],
      width: 600,
      height: 600,
      colors: ["#FFF5E4", "#FF7E65", "#7DCDFC", "#2084C4", "#3D444B"],
      margin: {
        top: 10,
        right: 10,
        bottom: 10,
        left: 10
      }
    });
  };

  d3.select("form select").on("change", function() {
    return showSunburst(this.options[this.selectedIndex].value);
  });

  showSunburst({{json|safe}});

});
window.require.register("demo/test", function(exports, require, module) {
  var answer1, answer2, answer3, answer4, pollChart;

  require("init");

  pollChart = window.pollChart;

  answer1 = [
    {
      id: 1,
      label: "Answer 1",
      value: 100,
      gender: {
        m: 30,
        f: 50
      },
      age: {
        "20s": 30,
        "30s": 20,
        "40s": 30
      }
    }, {
      id: 2,
      label: "Answer 2",
      value: 234,
      gender: {
        m: 50,
        f: 160
      },
      age: {
        "20s": 90,
        "30s": 100,
        "40s": 30
      }
    }, {
      id: 3,
      label: "Answer 3",
      value: 40,
      gender: {
        m: 10,
        f: 25
      },
      age: {
        "20s": 30,
        "30s": 2,
        "40s": 2
      }
    }, {
      id: 4,
      label: "Answer 4",
      value: 10,
      gender: {
        m: 1,
        f: 9
      },
      age: {
        "20s": 2,
        "30s": 5,
        "40s": 2
      }
    }, {
      id: 5,
      label: "Answer 5",
      value: 200,
      gender: {
        m: 30,
        f: 50
      },
      age: {
        "20s": 30,
        "30s": 20,
        "40s": 30
      }
    }
  ];

  answer2 = [
    {
      id: 1,
      label: "Answer 1",
      value: 100
    }, {
      id: 2,
      label: "Answer 2",
      value: 32
    }, {
      id: 3,
      label: "Answer 3",
      value: 40
    }, {
      id: 4,
      label: "Answer 4",
      value: 1
    }, {
      id: 5,
      label: "Answer 5",
      value: 23
    }
  ];

  answer3 = [
    {
      id: 1,
      label: "Answer 1",
      value: 20
    }, {
      id: 2,
      label: "Answer 2",
      value: 30
    }, {
      id: 3,
      label: "Answer 3",
      value: 40
    }, {
      id: 4,
      label: "Answer 4",
      value: 1
    }, {
      id: 5,
      label: "Answer 5",
      value: 6
    }
  ];

  answer4 = [
    {
      id: 1,
      label: "Answer 1",
      value: 100
    }, {
      id: 2,
      label: "Answer 2",
      value: 50
    }, {
      id: 3,
      label: "Answer 3",
      value: 10
    }, {
      id: 4,
      label: "Answer 4",
      value: 1
    }, {
      id: 5,
      label: "Answer 5",
      value: 500
    }
  ];

  pollChart.stacked({
    el: "#stacked",
    data: answer1
  });

  pollChart.stacked({
    el: "#stacked2",
    data: answer2
  });

  pollChart.grid({
    el: "#grid",
    data: [
      {
        question: "Some Question",
        answers: answer1,
        chosen: 1
      }, {
        question: "Some Question2",
        answers: answer2,
        chosen: 1
      }, {
        question: "Some Question3",
        answers: answer3,
        chosen: 1
      }, {
        question: "Some Question4",
        answers: answer4,
        chosen: 5
      }, {
        question: "Some Question5",
        answers: answer2,
        chosen: 2
      }
    ]
  });

});
window.require.register("grid", function(exports, require, module) {
  /*

    Grid Chart

    Data should be of the form:
    [
      {question: "Some Question"
       answers: [
        {id: 1, label: "Some Answer", value:2000}
        {id: 2, label: "Some Answer2", value:400}
        {id: 3, label: "Some Answer3", value:500}
       chosen: 2
    ]
  */

  var defaults, _ref;

  if ((_ref = window.pollChart) == null) {
    window.pollChart = {};
  }

  defaults = {
    width: 700,
    height: 60,
    margin: {
      top: 0,
      right: 0,
      bottom: 30,
      left: 0
    },
    colors: ["#FFF5E4", "#FF7E65", "#7DCDFC", "#2084C4", "#3D444B"],
    data: []
  };

  window.pollChart.grid = function(opts) {
    var answer, answers, chart, colors, data, el, get, getter, height, helpers, index, item, margin, pollChart, tooltip, width, _i, _j, _len, _len1, _ref1;

    pollChart = window.pollChart;
    helpers = pollChart.helpers;
    get = helpers.get;
    tooltip = pollChart.tooltip;
    opts = _.defaults(opts, defaults);
    margin = opts.margin, width = opts.width, height = opts.height;
    width = width - margin.left - margin.right;
    height = height - margin.top - margin.bottom;
    colors = opts.colors;
    data = [];
    _ref1 = opts.data;
    for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
      item = _ref1[_i];
      answers = _.sortBy(item.answers, "value");
      for (index = _j = 0, _len1 = answers.length; _j < _len1; index = ++_j) {
        answer = answers[index];
        if (answer.id === item.chosen) {
          data.push({
            question: item.question,
            answer: answer.label,
            color: colors[index]
          });
          break;
        }
      }
    }
    el = d3.select(opts.el);
    chart = el.selectAll(".gridSquare").data(data).enter().append("div").attr("class", "gridSquare").style("background", get("color"));
    getter = function(d) {
      return "Q. " + d.question + " <br />\nA. " + d.answer;
    };
    return tooltip(el, chart, getter);
  };

});
window.require.register("helpers", function(exports, require, module) {
  var _ref;

  if ((_ref = window.pollChart) == null) {
    window.pollChart = {};
  }

  window.pollChart.helpers = {
    get: function(key, fn) {
      return function(d) {
        var val;

        val = key ? d[key] : d;
        if (fn) {
          return fn(val);
        } else {
          return val;
        }
      };
    }
  };

});
window.require.register("init", function(exports, require, module) {
  require("./helpers");

  require("./legend");

  require("./legend2");

  require("./legend3");

  require("./tooltip");

  require("./tooltipBubble");

  require("./grid");

  require("./stacked");

  require("./sunburst");

});
window.require.register("legend", function(exports, require, module) {
  var _ref;

  if ((_ref = window.pollChart) == null) {
    window.pollChart = {};
  }

  window.pollChart.legend = function(_arg) {
    var colorKey, colorScale, data, el, g, holder, labelKey;

    colorScale = _arg.colorScale, el = _arg.el, data = _arg.data, labelKey = _arg.labelKey, colorKey = _arg.colorKey;
    if (colorKey == null) {
      colorKey = labelKey;
    }
    holder = el.append("div").attr("class", "legendHolder");
    g = holder.selectAll(".legend").data(data).enter().append("div").attr("class", "legend");
    g.append("span").style("background", function(d) {
      return colorScale(d[colorKey]);
    }).attr("class", "key");
    return g.append("span").text(function(d) {
      return d[labelKey];
    }).attr("class", "label");
  };

});
window.require.register("legend2", function(exports, require, module) {
  var _ref;

  if ((_ref = window.pollChart) == null) {
    window.pollChart = {};
  }

  window.pollChart.legend2 = function(_arg) {
    var colorKey, colorScale, data, el, g, getChecked, handler, holder, labelKey, valueKey;

    colorScale = _arg.colorScale, el = _arg.el, data = _arg.data, labelKey = _arg.labelKey, colorKey = _arg.colorKey, valueKey = _arg.valueKey, handler = _arg.handler;
    console.log(arguments);
    if (colorKey == null) {
      colorKey = labelKey;
    }
    if (handler == null) {
      handler = function() {};
    }
    getChecked = function() {
      data = _.compact(g.selectAll("input:checked").map(function(a) {
        var _ref1, _ref2;

        return (_ref1 = a[0]) != null ? (_ref2 = _ref1.__data__) != null ? _ref2[labelKey] : void 0 : void 0;
      }));
      if (data.length === 0) {
        this.checked = true;
        data = [this.__data__[labelKey]];
      }
      if (this.checked) {
        d3.select(this.parentNode).attr("class", "legend2").transition().duration(500).style("background-color", function(d) {
          return colorScale(d[colorKey]);
        });
      } else {
        d3.select(this.parentNode).attr("class", "legend2 disabled").transition().duration(500).style("background-color", "rgb(200,200,200)");
      }
      return handler(data);
    };
    holder = el.append("div").attr("class", "legendHolder");
    g = holder.selectAll(".legend2").data(data).enter().append("label").attr("class", "legend2").style("background-color", function(d) {
      return colorScale(d[colorKey]);
    });
    g.append("input").attr("type", "checkbox").attr("checked", "checked").on("change", getChecked);
    g.append("span").text(function(d) {
      return d[valueKey];
    }).attr("class", "value");
    return g.append("span").text(function(d) {
      return d[labelKey];
    }).attr("class", "label");
  };

});
window.require.register("legend3", function(exports, require, module) {
  var _ref;

  if ((_ref = window.pollChart) == null) {
    window.pollChart = {};
  }

  window.pollChart.legend3 = function(_arg) {
    var colorKey, colorScale, data, el, g, getChecked, handler, holder, labelKey, switcher, valueKey;

    colorScale = _arg.colorScale, el = _arg.el, data = _arg.data, labelKey = _arg.labelKey, colorKey = _arg.colorKey, valueKey = _arg.valueKey, handler = _arg.handler;
    console.log(arguments);
    if (colorKey == null) {
      colorKey = labelKey;
    }
    if (handler == null) {
      handler = function() {};
    }
    getChecked = function() {
      var $this;

      $this = d3.select(this).select(".switcher");
      if ($this.attr("class").indexOf("active") === -1) {
        $this.attr("class", "switcher active");
        d3.select(this).attr("class", "legend2").transition().duration(500).style("background-color", function(d) {
          return colorScale(d[colorKey]);
        });
      } else {
        $this.attr("class", "switcher");
        d3.select(this).attr("class", "legend2 disabled").transition().duration(500).style("background-color", "rgb(200,200,200)");
      }
      data = _.compact(g.selectAll(".active").map(function(a) {
        var _ref1, _ref2;

        return (_ref1 = a[0]) != null ? (_ref2 = _ref1.__data__) != null ? _ref2[labelKey] : void 0 : void 0;
      }));
      return handler(data);
    };
    holder = el.append("div").attr("class", "legendHolder");
    g = holder.selectAll(".legend2").data(data).enter().append("label").attr("class", "legend2").style("background-color", function(d) {
      return colorScale(d[colorKey]);
    }).on("click", getChecked);
    switcher = g.append("div").attr("class", "switcher active");
    switcher.append("span").attr("class", "onText").text("ON");
    switcher.append("span").attr("class", "offText").text("OFF");
    switcher.append("span").attr("class", "blackRect");
    g.append("span").text(function(d) {
      return d[valueKey];
    }).attr("class", "value");
    return g.append("span").text(function(d) {
      return d[labelKey];
    }).attr("class", "label");
  };

});
window.require.register("stacked", function(exports, require, module) {
  /*

    Horizontal Stacked Chart

    Data should be of the form:
    [
      {label: "Some Answer", value:2000}
    ]
  */

  var defaults, _ref;

  if ((_ref = window.pollChart) == null) {
    window.pollChart = {};
  }

  defaults = {
    width: 700,
    height: 60,
    margin: {
      top: 0,
      right: 0,
      bottom: 30,
      left: 0
    },
    colors: ["#FFF5E4", "#FF7E65", "#7DCDFC", "#2084C4", "#3D444B"],
    data: []
  };

  window.pollChart.stacked = function(opts) {
    var chart, color, data, el, get, group, height, helpers, item, margin, percent, pollChart, scale, start, svg, tooltip, total, width, _i, _len;

    pollChart = window.pollChart;
    helpers = pollChart.helpers;
    get = helpers.get;
    tooltip = pollChart.tooltip;
    opts = _.defaults(opts, defaults);
    margin = opts.margin, width = opts.width, height = opts.height, data = opts.data;
    width = width - margin.left - margin.right;
    height = height - margin.top - margin.bottom;
    total = d3.sum(data, get("value"));
    scale = d3.scale.linear().range([0, width]).domain([0, total]);
    color = d3.scale.ordinal().range(opts.colors);
    start = 0;
    for (_i = 0, _len = data.length; _i < _len; _i++) {
      item = data[_i];
      item.start = start;
      percent = Math.round(item.value / total * 100);
      item.tooltip = "" + item.label + " (" + percent + "%)";
      start += item.value;
    }
    el = d3.select(opts.el);
    svg = el.append("svg").attr("width", width + margin.left + margin.right).attr("height", height + margin.top + margin.bottom).append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    group = svg.selectAll("g").data(data, get("label")).enter().append("g");
    chart = group.append("rect").attr("class", "stack").style("fill", get("label", color)).attr("height", height).attr("x", get("start", scale)).attr("width", get("value", scale));
    return tooltip(el, chart, get("tooltip"));
  };

});
window.require.register("sunburst", function(exports, require, module) {
  /*

    Sunburst Chart

    Data should be of the form:
  */

  var defaults, get, getOptions, handle, log, sum, transformData, _ref,
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  if ((_ref = window.pollChart) == null) {
    window.pollChart = {};
  }

  defaults = {
    width: 600,
    height: 600,
    colors: ["#FFF5E4", "#FF7E65", "#7DCDFC", "#2084C4", "#3D444B"],
    margin: {
      top: 10,
      right: 10,
      bottom: 10,
      left: 10
    },
    data: [],
    labels: [],
    fields: []
  };

  sum = function(array, key) {
    var item, total, _i, _len;

    total = 0;
    for (_i = 0, _len = array.length; _i < _len; _i++) {
      item = array[_i];
      total += item[key];
    }
    return total;
  };

  get = function(key, fn) {
    return function(d) {
      var a;

      a = d[key];
      if (fn) {
        return fn(a);
      } else {
        return a;
      }
    };
  };

  handle = function(items, key, last, answer, total, parent) {
    var children, name, o, out, _ref1;

    out = [];
    _ref1 = _.groupBy(items, key);
    for (name in _ref1) {
      children = _ref1[name];
      o = {
        name: name,
        answer: answer
      };
      o.id = name + answer + key + parent.name;
      o.size = sum(children, "count");
      o.percent = "" + (Math.round(o.size / total * 100)) + "%";
      if (!last) {
        o.children = children;
      }
      out.push(o);
    }
    return out;
  };

  transformData = function(data, fields, answers) {
    var child, grandchild, item, o;

    if (fields == null) {
      fields = [];
    }
    if (answers == null) {
      answers = [];
    }
    return {
      name: data.question,
      children: (function() {
        var _i, _j, _k, _len, _len1, _len2, _ref1, _ref2, _ref3, _ref4, _results;

        _ref1 = data.answers;
        _results = [];
        for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
          item = _ref1[_i];
          if (!((_ref2 = item.answer, __indexOf.call(answers, _ref2) >= 0))) {
            continue;
          }
          o = {
            name: item.answer,
            answer: item.answer,
            size: item.count,
            id: item.answer,
            percent: "" + (Math.round(item.count / data.value * 100)) + "%"
          };
          if (fields.length) {
            o.children = handle(item.data, fields[0], fields.length === 1, item.answer, item.count, item);
            if (fields.length > 1) {
              _ref3 = o.children;
              for (_j = 0, _len1 = _ref3.length; _j < _len1; _j++) {
                child = _ref3[_j];
                child.children = handle(child.children, fields[1], fields.length === 2, item.answer, child.size, child);
                if (fields.length > 2) {
                  _ref4 = child.children;
                  for (_k = 0, _len2 = _ref4.length; _k < _len2; _k++) {
                    grandchild = _ref4[_k];
                    grandchild.children = handle(grandchild.children, fields[2], true, item.answer, grandchild.size, grandchild);
                  }
                }
              }
            }
          }
          _results.push(o);
        }
        return _results;
      })()
    };
  };

  log = function() {
    return console.log.apply(console, arguments);
  };

  getOptions = function(answers, field) {
    return _.chain(answers).pluck("data").flatten().pluck(field).unique().value();
  };

  window.pollChart.sunburst = function(opts) {
    var color, height, helpers, legend, margin, pollChart, radius, tooltip, width;

    pollChart = window.pollChart;
    helpers = pollChart.helpers;
    get = helpers.get;
    tooltip = pollChart.tooltipBubble;
    legend = pollChart.legend3;
    opts = _.defaults(opts, defaults);
    margin = opts.margin, width = opts.width, height = opts.height;
    width = width - margin.left - margin.right;
    height = height - margin.top - margin.bottom;
    radius = Math.min(width, height) / 2;
    color = d3.scale.ordinal().range(opts.colors);
    return d3.json(opts.src, function(err, root) {
      var answers, arc, change, clearHighlights, clickHandler1, clickHandler2, clicked, clicked2, data, divs, draw, draw4, el, field, filters, getSize, index, innerRadius, label, old, options, outerRadius, partition, selected, selects, svg, update, writeLabel, writeLabel2, _i, _len, _ref1, _ref2;

      answers = _.pluck(root.answers, "answer");
      data = transformData(root, [], answers);
      options = [];
      _ref1 = opts.fields;
      for (index = _i = 0, _len = _ref1.length; _i < _len; index = ++_i) {
        field = _ref1[index];
        label = (_ref2 = opts.labels[index]) != null ? _ref2 : field;
        options.push({
          label: label,
          field: field
        });
      }
      options = ["Blank"].concat(_.compact(options));
      partition = d3.layout.partition().sort(null).size([2 * Math.PI, radius * radius * 0.5]).value(get("size"));
      innerRadius = function(d) {
        if (d.depth === 1) {
          return 0;
        } else {
          return Math.sqrt(d.y);
        }
      };
      outerRadius = function(d) {
        return Math.sqrt(d.y + d.dy);
      };
      arc = d3.svg.arc().startAngle(function(d) {
        return d.x;
      }).endAngle(function(d) {
        return d.x + d.dx;
      }).innerRadius(innerRadius).outerRadius(outerRadius);
      el = d3.select(opts.el);
      el.append("h2").text(root.question);
      el.append("p").text(root.value + " Answers");
      svg = el.append("svg").attr("width", width + margin.left + margin.right).attr("height", height + margin.top + margin.bottom).append("g").attr("transform", "translate(" + width / 2 + "," + height * .52 + ")");
      label = el.append("span").attr("class", "poll-label");
      old = null;
      clicked = [];
      clicked2 = [];
      clickHandler2 = function(d2) {
        var $grandparent, $parent, $this, group, parents, turnOff, wrongParent;

        $this = d3.select(this);
        group = svg.selectAll("g");
        $parent = group.filter(function(d) {
          return d === d2.parent;
        });
        $grandparent = group.filter(function(d) {
          return d === d2.parent.parent;
        });
        if (__indexOf.call(clicked2, d2) >= 0) {
          clicked2 = _.without(clicked2, d2);
          $this.attr("opacity", 1);
        } else {
          clicked2.push(d2);
          $this.attr("opacity", 0.7);
          wrongParent = _.filter(clicked2, function(d) {
            return d.parent.parent !== d2.parent.parent;
          });
          console.log({
            wrongParent: wrongParent
          });
          if (wrongParent.length) {
            clicked2 = _.difference(clicked2, wrongParent);
            group.filter(function(d) {
              return __indexOf.call(wrongParent, d) >= 0;
            }).attr("opacity", 1);
          }
          parents = _.pluck(clicked2, "parent");
          turnOff = _.difference(clicked, parents);
          if (turnOff.length) {
            turnOff = turnOff.concat(_.pluck(turnOff, "parent"));
            group.filter(function(d) {
              return __indexOf.call(turnOff, d) >= 0;
            }).attr("opacity", 1);
          }
          clicked = [d2.parent];
          $parent.attr("opacity", 0.7);
          $grandparent.attr("opacity", 0.7);
        }
        if (clicked2.length) {
          return writeLabel2();
        } else {
          return writeLabel();
        }
      };
      getSize = function(d) {
        return d.size;
      };
      writeLabel = function() {
        var grouped, key, keySum, out, total, vals;

        out = "";
        total = d3.sum(_.unique(_.pluck(clicked, "parent")), getSize);
        grouped = _.groupBy(clicked, "name");
        for (key in grouped) {
          vals = grouped[key];
          keySum = d3.sum(vals, getSize);
          out += "" + key + " - (" + (Math.round(keySum / total * 100)) + "%) ";
        }
        return label.text(out);
      };
      writeLabel2 = function() {
        var grouped, key, keySum, out, total, vals;

        out = "";
        total = d3.sum(_.unique(_.pluck(clicked2, "parent")), getSize);
        grouped = _.groupBy(clicked2, "name");
        for (key in grouped) {
          vals = grouped[key];
          keySum = d3.sum(vals, getSize);
          out += "" + key + " - (" + (Math.round(keySum / total * 100)) + "%) ";
        }
        return label.text(out);
      };
      clickHandler1 = function(d1) {
        var $parent, $this, _ref3;

        $this = d3.select(this);
        $parent = svg.selectAll("g").filter(function(d) {
          return d === d1.parent;
        });
        if (__indexOf.call(clicked, d1) >= 0) {
          clicked = _.without(clicked, d1, d1.parent);
          $this.attr("opacity", 1);
          if (_ref3 = d1.parent, __indexOf.call(_.pluck(clicked, "parent"), _ref3) < 0) {
            $parent.attr("opacity", 1);
          }
        } else {
          clicked.push(d1);
          $this.attr("opacity", 0.7);
          $parent.attr("opacity", 0.7);
        }
        if (clicked2.length) {
          svg.selectAll("g").filter(function(d) {
            return __indexOf.call(clicked2, d) >= 0;
          }).attr("opacity", 1);
          clicked2 = [];
        }
        return writeLabel();
      };
      clearHighlights = function() {
        clicked = [];
        clicked2 = [];
        label.text("");
        return svg.selectAll("g").attr("opacity", 1);
      };
      draw = function(data) {
        var group, insertLinebreaks, kuler, textTransform;

        kuler = function(d) {
          return color(d.answer);
        };
        data = partition.nodes(data);
        window.dave = data;
        svg.selectAll("g").remove();
        group = svg.selectAll("g").data(data, get("id")).enter().append("g");
        group.filter(function(d) {
          return d.depth;
        }).append("path").style("stroke", "#fff").style("fill", kuler).attr("d", arc);
        textTransform = function(d) {
          var c, h, x, y;

          c = arc.centroid(d);
          x = c[0];
          y = c[1];
          h = Math.sqrt(x * x + y * y);
          return "translate(" + (x / h * radius * 0.9) + "," + (y / h * radius * 0.9) + ")";
        };
        insertLinebreaks = function(d) {
          var i, textElem, tspan, word, words, _ref3, _ref4, _ref5, _results;

          textElem = d3.select(this);
          words = d.name.split(" ");
          textElem.text("");
          i = 0;
          _results = [];
          while (words.length) {
            word = [(_ref3 = words.shift()) != null ? _ref3 : "", (_ref4 = words.shift()) != null ? _ref4 : "", (_ref5 = words.shift()) != null ? _ref5 : ""].join(" ");
            tspan = textElem.append("tspan").text(word);
            if (i > 0) {
              tspan.attr("x", 0).attr("dy", "15");
            }
            _results.push(i++);
          }
          return _results;
        };
        group.filter(function(d) {
          return d.depth === 1;
        }).append("text").text(function(d) {
          return d.name;
        }).attr("dy", ".35em").style("text-anchor", "middle").attr("transform", textTransform).each(insertLinebreaks);
        group.filter(function(d) {
          return d.depth === 3;
        }).on("click", clickHandler2);
        group.filter(function(d) {
          return d.depth === 2;
        }).on("click", clickHandler1);
        return group.filter(function(d) {
          return d.depth === 1;
        }).on("click", clearHighlights);
      };
      draw4 = function(data) {
        var enter, group, paths, tran, tweenArc;

        data = partition.nodes(data);
        group = svg.selectAll("g").data(data, get("id"));
        enter = group.enter().append("g");
        enter.filter(function(d) {
          return d.depth;
        }).append("path").style("stroke", "#fff").style("fill", "#fff");
        enter.filter(function(d) {
          return d.depth === 1;
        }).append("text").text(function(d) {
          return d.name;
        }).attr("dy", ".35em").style("text-anchor", "middle");
        paths = group.selectAll("path");
        tran = paths.transition().duration(1000).style("fill", get("answer", color));
        if (old) {
          tweenArc = function(a) {
            var end, i, start;

            if (old && old[a.id]) {
              start = _.pick(old[a.id][0], "x", "y", "dy", "y", "depth");
            } else {
              start = {
                x: 0,
                dx: 0,
                y: 0,
                dy: 0,
                depth: 0
              };
            }
            end = {
              x: a.x,
              dx: a.dx,
              y: a.y,
              dy: a.dy,
              depth: a.depth
            };
            i = d3.interpolate(start, end);
            return function(t) {
              return arc(i(t));
            };
          };
          tran.attrTween("d", tweenArc);
        } else {
          tran.attr("d", arc);
        }
        group.select("text").transition().duration(1000).attr("transform", function(d) {
          return "translate(" + arc.centroid(d) + ")";
        });
        group.exit().remove();
        return old = _.groupBy(data, "id");
      };
      draw(data);
      legend({
        el: el,
        colorScale: color,
        data: data.children,
        labelKey: "name",
        colorKey: "answer",
        valueKey: "percent",
        handler: function(data) {
          answers = data;
          return update();
        }
      });
      filters = [
        {
          options: options
        }, {
          options: options
        }
      ];
      el.append("h4").text("Filters: ");
      divs = el.selectAll(".filter").data(filters).enter().append("div").attr("class", "filter");
      selected = [];
      change = function(d, i) {
        selected[i] = this.options[this.selectedIndex].__data__.field;
        return update();
      };
      selects = divs.append("select").on("change", change);
      selects.selectAll("option").data(get("options")).enter().append("option").text(get("label"));
      return update = function() {
        data = transformData(root, _.compact(selected), answers);
        return draw(data);
      };
    });
  };

});
window.require.register("tooltip", function(exports, require, module) {
  var _ref;

  if ((_ref = window.pollChart) == null) {
    window.pollChart = {};
  }

  window.pollChart.tooltip = function(parent, selection, getter) {
    var tooltip, tooltipMove, tooltipOut, tooltipOver;

    tooltip = d3.select('body').append("div").attr("class", "tooltip").style("opacity", 0);
    tooltipOver = function(d) {
      d3.select(this).style({
        "opacity": 0.8
      });
      tooltip.transition().duration(200).style("opacity", 0.9);
      return tooltip.html(getter(d));
    };
    tooltipMove = function() {
      return tooltip.style("left", (d3.event.pageX + 10) + "px").style("top", (d3.event.pageY - 10) + "px");
    };
    tooltipOut = function() {
      d3.select(this).style({
        "opacity": 1
      });
      return tooltip.transition().duration(200).style("opacity", 0);
    };
    return selection.on("mouseover", tooltipOver).on("mouseout", tooltipOut).on("mousemove", tooltipMove);
  };

});
window.require.register("tooltipBubble", function(exports, require, module) {
  var _ref;

  if ((_ref = window.pollChart) == null) {
    window.pollChart = {};
  }

  window.pollChart.tooltipBubble = function(parent, selection, getter) {
    var span, svg, tooltip, tooltipMove, tooltipOut, tooltipOver;

    tooltip = d3.select("body").append("div").attr("class", "tooltip").style("opacity", 0);
    span = tooltip.append("span");
    svg = tooltip.append("svg");
    svg.append("path").attr("class", "tooltip").attr("d", d3.svg.symbol("triangle-down"));
    tooltipOver = function(d) {
      d3.select(this).style({
        "opacity": 0.7
      });
      tooltip.transition().duration(200).style("opacity", 0.9);
      return span.html(getter(d));
    };
    tooltipMove = function() {
      return tooltip.style("left", (d3.event.layerX + 20) + "px").style("top", (d3.event.layerY - 10) + "px");
    };
    tooltipOut = function() {
      d3.select(this).style({
        "opacity": 1
      });
      return tooltip.transition().duration(200).style("opacity", 0);
    };
    return selection.on("mouseover", tooltipOver).on("mouseout", tooltipOut).on("mousemove", tooltipMove);
  };

});
