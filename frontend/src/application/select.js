import TomSelect from "tom-select";
import * as Popper from "@popperjs/core";


window.TomSelect = function createDynamicTomSelect(element) {
  // Basic configuration
  const config = {
    plugins: {},

    // Extract 'create' option from data attribute
    create: element.dataset.create === 'true',

    allowEmptyOption: element.dataset.allowEmptyOption === 'true',
    render: {
        no_results: function () {
            return `<div class="no-results">${element.dataset.txtNoResults || 'No results...'}</div>`;
        },
        option_create: function(data, escape) {
			return `<div class="create">${element.dataset.txtCreate || 'Add'} <strong>${escape(data.input)}</strong>&hellip;</div>`;
		},
    },

    onInitialize: function () {
        this.popper = Popper.createPopper(this.control, this.dropdown, {
            placement: "bottom-start",
            modifiers: [
                {
                    name: "sameWidth",
                    enabled: true,
                    fn: ({state}) => {
                        state.styles.popper.width = `${state.rects.reference.width}px`;
                    },
                    phase: "beforeWrite",
                    requires: ["computeStyles"],
                },
                {
                    name: 'flip',
                    options: {
                      fallbackPlacements: ['top-start'],
                    },
               },
            ]

        });

    },
    onDropdownOpen: function () {
        this.popper.update();
    }
  };

  if (element.dataset.checkboxes === 'true') {
      config.plugins.checkbox_options = {
            'checkedClassNames': ['ts-checked'],
            'uncheckedClassNames': ['ts-unchecked'],
        };
  }

  if (element.dataset.clearButton === 'true') {
      config.plugins.clear_button = {
            'title': element.dataset.txtClear || 'Clear',
        };
  }

  if (element.dataset.removeButton === 'true') {
      config.plugins.remove_button = {
            'title': element.dataset.txtRemove || 'Remove',
        };
  }

  // Create and return the TomSelect instance
  return new TomSelect(element, config);
};
