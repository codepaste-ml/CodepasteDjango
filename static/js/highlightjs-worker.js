onmessage = function (event) {
    var {source, libPath} = JSON.parse(event.data);
    importScripts(libPath);
    self.hljs.configure({
        tabReplace: '    ',
        useBR: true
    });

    var result = {};
    if(source.language === 'auto') {
        result = self.hljs.highlightAuto(source.source);
    } else {
        result = self.hljs.highlight(source.language, source.source, true);
    }
    result = self.hljs.fixMarkup(result.value);

    postMessage(result);
};