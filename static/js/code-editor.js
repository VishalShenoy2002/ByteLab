require(['vs/editor/editor.main'], function () {
    var codeEditor = document.getElementById('code-editor');
    var languageLabel = document.getElementById('language-label');
    var questionIdLabel = document.getElementById('question-id-label');
    var language = languageLabel.textContent.toLowerCase();
    var questionId = questionIdLabel.textContent.toLowerCase();
    var question = document.getElementById('question-text').textContent.toLowerCase();
    console.log(language);

    var appColors = getComputedStyle(document.documentElement);
    var backgroundColor = appColors.getPropertyValue("--background");
    var textColor = appColors.getPropertyValue("--text");
    var primaryColor = appColors.getPropertyValue("--primary");
    var secondaryColor = appColors.getPropertyValue("--secondary");
    var accentColor = appColors.getPropertyValue("--accent");

    console.log(backgroundColor);
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
    };

    monaco.editor.defineTheme('bytelab-dark', themeParameters);

    parameters = {
        language: language,
        lineNumbers: 'on',
        vertical: 'auto',
        horizontal: 'auto',
        minimap: {
            enabled: true
        },
        theme: 'bytelab-dark',
        'bracketPairColorization.enabled': false,
    };

    var editor = monaco.editor.create(codeEditor, parameters);

    function sendCodeToFlask(editor) {
        var code = editor.getValue();
        var language = languageLabel.textContent.toLowerCase();
        fetch('/submit', {
            method: "POST",
            body: new URLSearchParams({
                code: code,
                language: language,
                question_id: questionId,
                question: question
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            console.log(data);
            // Redirect to student-dashboard/solve-questions
            window.location.href = '/student-dashboard/solve-questions';
        })
        .catch(error => {
            console.error('Error', error);
        });
    }

    var submitButton = document.getElementById('submit-button');
    submitButton.addEventListener('click', function () {
        console.log("click");
        sendCodeToFlask(editor);
    });
});
