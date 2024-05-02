require(['vs/editor/editor.main'], function (){
    var codeEditor = document.getElementById('code-editor')
    var languageLabel = document.getElementById('language-label')
    var language = languageLabel.textContent.toLowerCase()
    console.log(language)

    
    var appColors = getComputedStyle(document.documentElement)
    var backgroundColor = appColors.getPropertyValue("--background")
    var textColor = appColors.getPropertyValue("--text")
    var primaryColor = appColors.getPropertyValue("--primary")
    var secondaryColor = appColors.getPropertyValue("--secondary")
    var accentColor = appColors.getPropertyValue("--accent")


    console.log(backgroundColor)
    themeParameters = {
        base: 'vs',
        inherit: true,
        rules: [
            {
                token: "comment",
                foreground: secondaryColor,
                fontStyle: "italic"
            },
            {
                token: "delimiter",
                foreground: secondaryColor,
                fontStyle: ""
            },

            {
                token: "operator",
                foreground: secondaryColor,
                fontStyle: "italic"
            },
            {
                token: "keyword",
                foreground: accentColor,
                fontStyle: "italic"
            },
            {
                token: "number",
                foreground: primaryColor
            },
            {
                token: "string",
                foreground: primaryColor
            },
            {
                token: "entity",
                foreground: "#ff0000"
            }
        ],

        colors: {
            'editor.background': backgroundColor,
            'editor.foreground': textColor,
            'editorLineNumber.activeForeground': accentColor,
            'editorLineNumber.foreground': textColor,
            'editor.lineHighlightBorder': backgroundColor,
            'editorSuggestWidget.selectedBackground': secondaryColor,
            'editorSuggestWidget.background': backgroundColor,
            'editorSuggestWidget.foreground': primaryColor,
            'editorCursor.foreground': secondaryColor,
            'textSeparator.foreground': primaryColor,
        },
    }
    
    monaco.editor.defineTheme('bytelab-dark',themeParameters)
    
    parameters ={
        language: language,
        lineNumbers: 'on',
        vertical: 'auto',
        horizontal: 'auto',
        minimap:{
            enabled: true
        },
        theme:'bytelab-dark',
        'bracketPairColorization.enabled': false,

        
    }
    var editor = monaco.editor.create(codeEditor,parameters)

    function sendCodeToFlask(editor){
        var code = editor.getValue()
        var language = languageSelector.value
        fetch('/save',{
            method: "POST",
            body: new URLSearchParams({
                code: code,
                language: language
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).then(response => response.text).then(data => {
            console.log(data);
    
        }).catch(error => {
            console.error('Error',error);
        })
    
    
    }
    var submitButton = document.getElementById('submit-code')
    submitButton.addEventListener('click', function () {
        sendCodeToFlask(editor)
    })
})
