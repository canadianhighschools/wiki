// utilities
var get = function (selector, scope) {
    scope = scope ? scope : document;
    return scope.querySelector(selector);
};

var getAll = function (selector, scope) {
    scope = scope ? scope : document;
    return scope.querySelectorAll(selector);
};


function get_indent_of_link(el) {
    const indent = el.getAttribute('data-indent')
    
    if (indent) {
        return parseInt(indent)
    }
    return NaN
}

function create_link_indents() {
    const table = get('#doc__toc')
    if (table) {
        const items = getAll('.toc__item', table)

        for (let i = 0; i < items.length; i++) {
            const k = items[i]

            const indent = get_indent_of_link(k)
            // alert (i + ' ' + indent + ' ' + (items.length-1))

            if (indent) {
                const anchor = get('a', k)
                if (anchor) {
                    anchor.innerHTML = ' ' + anchor.textContent
                    k.style.marginLeft = 20*indent + 'px';

                    // if next element has less indent
                    if (i !== (items.length-1)) {
                        // alert (i + ' ' + indent + ' ' + (i === items.length-1))
                        const z = items[i+1]
                        const i2 = get_indent_of_link(z)

                        if (i2 && i2 > indent) {
                            anchor.textContent = '▾' + anchor.textContent
                            anchor.style.fontWeight = 'bold';
                            k.style.marginLeft = 15*indent + 'px';
                        }
                    }
                }
            }
        }
    }

}

create_link_indents()