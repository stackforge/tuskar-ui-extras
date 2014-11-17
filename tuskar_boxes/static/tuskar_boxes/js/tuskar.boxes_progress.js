tuskar.boxes_progress = function () {
  'use static';
  var module = {};

  module.init = function () {
    this.nodes_template = Hogan.compile($('#nodes-template').html() || '');
  };

  module.update_progress = function (data) {
    $('div.boxes-nodes').html(module.nodes_template.render(data));
  };

  // Attach to the original update procedure.
  var orig_update_progress = tuskar.deployment_progress.update_progress;
  tuskar.deployment_progress.update_progress = function () {
    orig_update_progress.apply(this, arguments);
    module.update_progress.apply(module, arguments);
  };

  horizon.addInitFunction(module.init);
  return module;
} ();
