import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    console.log('Congratulations, your extension "aider" is now active!');

    let disposable = vscode.commands.registerCommand('aider.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World from Aider!');
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
