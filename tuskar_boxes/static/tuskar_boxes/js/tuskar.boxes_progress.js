/* global $ tuskar horizon Hogan */
tuskar.boxesProgress = function() {
  "use strict";
  "use static";

  var module = {};

  module.init = function() {
    module.nodesTemplate = Hogan.compile($("#nodes-template").html() || "");
  };

  module.updateProgress = function (data) {
    $("div.boxes-nodes").html(module.nodesTemplate.render(data));
  };

  // Attach to the original update procedure.
  var origUpdateProgress = tuskar.deployment_progress.updateProgress;
  tuskar.deployment_progress.updateProgress = function() {
    origUpdateProgress.apply(tuskar.deployment_progress, arguments);
    module.updateProgress.apply(module, arguments);
  };

  horizon.addInitFunction(module.init);
  return module;
}();
