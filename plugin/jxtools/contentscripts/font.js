(function () {

    var pvft = '(' + function () {
        'use strict';
        function defineobjectproperty(val, e, c, w) {

            return {
                value: val,
                enumerable: !!e,
                configurable: !!c,
                writable: !!w
            }
        }

        var originalStyleSetProperty = CSSStyleDeclaration.prototype.setProperty
        var originalSetAttrib = Element.prototype.setAttribute
        var originalNodeAppendChild = Node.prototype.appendChild

        var DEFAULT = 'auto';

        var baseFonts = ['default']

        var FontWhiteList = ["Arial", "Arial Black", "Arial Narrow", "Calibri", "Calibri Light", "Cambria", "Cambria Math", "Candara", "Caurier Regular", "Comic Sans", "Comic Sans MS", "Comic Sans MS Bold", "Consolas", "Constantia", "Corbel", "Courier", "Courier New", "cursive", "Ebrima", "fantasy", "Fixedsys", "Fixedsys Regular", "Franklin Gothic", "Franklin Gothic Medium", "Gabriola", "Gabriola Regular", "Gadugi", "Georgia", "Helvetica", "HoloLens MDL2 Assets", "HoloLens MDL2 Assets Regular", "Impact", "Impact Regular", "Javanese Text", "Javanese Text Regular", "Leelawadee UI", "Leelawadee UI Semilight", "Lucida Console", "Lucida Console Regular", "Lucida Sans Unicode", "Lucida Sans Unicode Regular", "Malgun Gothic", "Malgun Gothic Semilight", "Marlett", "Microsoft Himalaya", "Microsoft Himalaya Regular", "Microsoft JhengHei", "Microsoft JhengHei Light", "Microsoft JhengHei UI", "Microsoft JhengHei UI Light", "Microsoft New Tai Lue", "Microsoft PhagsPa", "Microsoft PhangsPa", "Microsoft Sans Serif", "Microsoft Sans Serif Regular", "Microsoft Tai Le", "Microsoft YaHei", "Microsoft YaHei Light", "Microsoft YaHei UI", "Microsoft YaHei UI Light", "Microsoft Yi Baiti", "Microsoft Yi Baiti Regular", "MingLiU-ExtB", "MingLiu-ExtB Regular", "MingLiU_HKSCS-ExtB", "MingLiU_HKSCS-ExtB Regular", "Modern", "Modern Regular", "Mongolia Baiti Regular", "Mongolian Baiti", "monospace", "MS Gothic", "MS Gothic Regular", "MS PGothic", "MS PGothic Regular", "MS Sans Serif", "MS Sans Serif Regular", "MS Serif", "MS Serif Regular", "MS UI Gothic", "MS UI Gothic Regular", "MV Boli", "MV Boli Regular", "Myanmar Tet", "Myanmar Text", "Nimarla UI", "Nirmala UI", "Nirmala UI Semilight", "NSimSun", "NSimSun Regular", "Palatino Linotype", "PMingLiU-ExtB", "PMingLiU-ExtB Regular", "Roman", "Roman Regular", "sans-serif", "Script", "Script Regular", "Segoe MDL2 Assets", "Segoe MDL2 Assets Regular", "Segoe Print", "Segoe Script", "Segoe UI", "Segoe UI Black", "Segoe UI Emoji", "Segoe UI Emoji Regular", "Segoe UI Historic", "Segoe UI Historic Regular", "Segoe UI Light", "Segoe UI Semibold", "Segoe UI Semilight", "Segoe UI Symbol", "Segoe UI Symbol Regular", "serif", "SimSun", "SimSun-ExtB", "SimSun-ExtB Regular", "SimSun Regular", "Sitka Banner", "Sitka Display", "Sitka Heading", "Sitka Small", "Sitka Subheading", "Sitka Text", "Small Fonts", "Small Fonts Regular", "Sylfaen", "Sylfaen Regular", "Symbol", "Symbol Regular", "System", "System Bold", "Tahoma", "Terminal", "Times", "Times New Roman", "Trebuchet MS", "Verdana", "Webdings", "Webdings Regular", "Wingdings", "Wingdings 2", "Wingdings 3", "Wingdings Regular", "Yu Gothic", "Yu Gothic Light", "Yu Gothic Medium", "Yu Gothic UI", "Yu Gothic UI Light", "Yu Gothic UI Semibold", "Yu Gothic UI Semilight", "Brush Script MT", "Broadway", "Bell MT", "Berlin Sans FB", "Blackadder ITC", "Curlz MT", "Elephant", "Engravers MT", "Goudy Old Style", "Lucida Fax", "MS Outlook", "Minion Pro", "Papyrus", "Wide Latin", "Snap ITC", "Stencil", "Old English Text MT"].map(function (x) { return x.toLowerCase() })

        var keywords = ['inherit', 'auto', 'default', '!Important']

        baseFonts.push.apply(baseFonts, FontWhiteList)
        baseFonts.push.apply(baseFonts, keywords)

        function getAllowedFontFamily(family) {
            var fonts = family.replace(/"|'/g, '').split(',')
            var allowedFonts = fonts.filter(function (font) {
                if (font && font.length) {
                    var normalised = font.trim().toLowerCase()

                    for (var allowed of baseFonts)
                        if (normalised == allowed) return true

                    for (var allowed of document.fonts.values())
                        if (normalised == allowed) return true
                }
            })
            return allowedFonts.map(function (f) {
                var trimmed = f.trim()
                return ~trimmed.indexOf(' ') ? "'" + trimmed + "'" : trimmed
            }).join(", ")
        }

        var offsetArr = [[font]]
        var offsetIdx = 0;

        function modifiedCssSetProperty(key, val) {
            if (key.toLowerCase() == 'font-family') {
                var keyresult = key.toLowerCase()

                var mrrandom = offsetArr[offsetIdx]
                offsetIdx = (offsetIdx + 1) % offsetArr.length
                //Math.floor(Math.random() * 10);
                if (mrrandom < 7) {
                    var allowed = getAllowedFontFamily(val)
                    var oldFF = this.fontFamily
                } else {
                    var allowed = oldFF
                    var oldFF = getAllowedFontFamily(val)
                }

                return originalStyleSetProperty.call(this, 'font-family', allowed || DEFAULT)
            }
            return originalStyleSetProperty.call(this, key, val)
        }

        function makeModifiedSetCssText(originalSetCssText) {
            return function modifiedSetCssText(css) {
                var fontFamilyMatch = css.match(/\b(?:font-family:([^;]+)(?:;|$))/i)
                if (fontFamilyMatch && fontFamilyMatch.length == 1) {
                    css = css.replace(/\b(font-family:[^;]+(;|$))/i, '').trim()
                    var allowed = getAllowedFontFamily(fontFamilyMatch[1]) || DEFAULT
                    if (css.length && css[css.length - 1] != ';')
                        css += ';'
                    css += "font-family: " + allowed + ";"
                }
                return originalSetCssText.call(this, css)
            }
        }

        var modifiedSetAttribute = (function () {
            var innerModify = makeModifiedSetCssText(function (val) {
                return originalSetAttrib.call(this, 'style', val)
            })
            return function modifiedSetAttribute(key, val) {
                if (key.toLowerCase() == 'style') {
                    return innerModify.call(this, val)
                }
                return originalSetAttrib.call(this, key, val)
            }
        })();

        function makeModifiedInnerHTML(originalInnerHTML) {
            return function modifiedInnerHTML(html) {

                var retval = originalInnerHTML.call(this, html)
                recursivelyModifyFonts(this.parentNode)
                return retval
            }
        }

        function recursivelyModifyFonts(elem) {
            if (elem) {
                if (elem.style && elem.style.fontFamily) {
                    modifiedCssSetProperty.call(elem.style, 'font-family', elem.style.fontFamily)
                }
                if (elem.childNodes) {
                    for (var i = 0; i < elem.childNodes.length; i++) {
                        recursivelyModifyFonts(elem.childNodes[i]);
                    }
                }
            }
            return elem
        }

        function modifiedAppend(child) {
            child = recursivelyModifyFonts(child)
            return originalNodeAppendChild.call(this, child)
        }

        var success = true

        function overrideFunc(obj, name, f) {
            try {
                Object.defineProperty(obj.prototype, name, defineobjectproperty(f, true))
            } catch (e) { success = false; }
        }

        function overrideSetter(obj, name, makeSetter) {
            try {
                var current = Object.getOwnPropertyDescriptor(obj.prototype, name)
                current.set = makeSetter(current.set)
                current.configurable = false
                Object.defineProperty(obj.prototype, name, current)
            } catch (e) { success = false; }
        }
        overrideFunc(Node, 'appendChild', modifiedAppend)
        overrideFunc(CSSStyleDeclaration, 'setProperty', modifiedCssSetProperty)
        overrideFunc(Element, 'setAttribute', modifiedSetAttribute)

        try {
            Object.defineProperty(CSSStyleDeclaration.prototype, 'fontFamily', {
                set: function fontFamily(f) {
                    modifiedCssSetProperty.call(this, 'font-family', f)
                },
                get: function fontFamily() {
                    return this.getPropertyValue('font-family')
                }
            })
        } catch (e) { success = false; }


        overrideSetter(CSSStyleDeclaration, 'cssText', makeModifiedSetCssText)
        overrideSetter(Element, 'innerHTML', makeModifiedInnerHTML)
        overrideSetter(Element, 'outerHTML', makeModifiedInnerHTML)

    } + ')();';

    var script = document.createElement('script')
    script.textContent = pvft;
    (document.head || document.documentElement).appendChild(script)
    script.parentNode.removeChild(script)

})();