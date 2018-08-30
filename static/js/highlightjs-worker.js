onmessage = function (event) {
    var {source, libPath} = JSON.parse(event.data);
    importScripts(libPath);
    self.hljs.configure({
        tabReplace: '    ',
        useBR: true
    });

    var result = {};
    if(source.source_lang === 'auto') {
        result = self.hljs.highlightAuto(source.source_source);
    } else {
        result = self.hljs.highlight(source.source_lang, source.source_source, true);
    }
    result = self.hljs.fixMarkup(result.value);

    postMessage(result);
};