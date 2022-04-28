var style = document.createElement('style');
style.innerText = "#pannel{transition:transform .3s ease}#pannel[data-pannel=open]>#pannelAction>svg{transform:rotate(90deg)}#pannel[data-pannel=close]{transform:translateY(100%)}#pannel[data-pannel=close]>#pannelAction>svg{transform:rotate(270deg)}#pannelAction{position:absolute;top:-28px;right:0;display:flex;align-items:center;justify-content:center;padding:6px 10px;font-size:24px;background-color:rgba(0,0,0,.5);cursor:pointer}#pannelAction>svg{width:16px;height:16px;fill:#fff;transition:transform .3s ease}";
document.head.appendChild(style);

var bottominfo_inject = function () {
    var arr = [[bottominfobar]];
    var ul = document.createElement('ul');
    ul.setAttribute('id', 'pannel');
    ul.setAttribute('data-pannel', 'open');
    ul.style = "bottom: 0px; left: 0px; right: 0px; background-color: rgba(0, 0, 0, 0.5); position: fixed; padding: 5px; z-index: 99999; margin: 0px; font-family: sans-serif; font-size: 20px; list-style: none;list-style-type: none;";
    for (var i = 0; i < arr.length; i++) {
        var carr = arr[i];
        var li = document.createElement('li');
        li.style = "float: left;padding:0px; margin:0px; margin-right: 10px; color:#fff;";
        li.innerHTML = carr[0] + ": " + carr[1];
        ul.appendChild(li);
    }
    var pannel = document.createElement('li');
    pannel.setAttribute('id', 'pannelAction');
    pannel.innerHTML = "<svg viewBox=\"64 64 896 896\" focusable=\"false\" data-icon=\"right\" width=\"1em\" height=\"1em\" fill=\"currentColor\" aria-hidden=\"true\"><path d=\"M765.7 486.8L314.9 134.7A7.97 7.97 0 00302 141v77.3c0 4.9 2.3 9.6 6.1 12.6l360 281.1-360 281.1c-3.9 3-6.1 7.7-6.1 12.6V883c0 6.7 7.7 10.4 12.9 6.3l450.8-352.1a31.96 31.96 0 000-50.4z\"></path></svg>";
    ul.insertAdjacentElement('afterbegin', pannel);
    document.body.appendChild(ul);
};

var bottominfo_script_1 = document.createElement('script');
bottominfo_script_1.textContent = "(" + bottominfo_inject + ")()";
document.documentElement.appendChild(bottominfo_script_1);

document.getElementById('pannelAction').addEventListener('click', function (e) {
    var oPannel = document.getElementById('pannel');
    if (oPannel.dataset.pannel === 'close') return oPannel.dataset.pannel = 'open';
    return oPannel.dataset.pannel = 'close';
});