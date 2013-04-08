$('document').ready(function(){
    var editor = new TINY.editor.edit('editor', {
        id: 'id_body',
        width: 584,
        height: 175,
        cssclass: 'tinyeditor',
        controlclass: 'tinyeditor-control',
        rowclass: 'tinyeditor-header',
        dividerclass: 'tinyeditor-divider',
        controls: ['bold', 'italic', 'underline', 'strikethrough', '|', 'subscript', 'superscript', '|',
            'orderedlist', 'unorderedlist', '|', 'outdent', 'indent', '|', 'leftalign',
            'centeralign', 'rightalign', 'blockjustify', '|', 'unformat', '|', 'undo', 'redo', 'n',
            'font', 'size', 'style', '|', 'image', 'hr', 'link', 'unlink', '|', 'print'],
        footer: true,
        fonts: ['Verdana','Arial','Georgia','Trebuchet MS'],
        xhtml: true,
        bodyid: 'editor',
        footerclass: 'tinyeditor-footer',
        toggle: {text: 'source', activetext: 'wysiwyg', cssclass: 'toggle'},
        resize: {cssclass: 'resize'}
    });
   $('input[id*="publish_date"]').datepicker();
});