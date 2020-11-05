// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode'); 
const { spawn } = require('child_process')

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */

function showQueryAndResultAsVsMessage(query, result)
{
	vscode.window.showInformationMessage(`your Query: ${query} | your Result: ${result}`);
}

function callPythonScript(script, args)
{
	var pythonCommand = (process.platform == "linux") ? 'python3' : 'python';
	console.log(process.platform);
	console.log(pythonCommand);
	const sensor = spawn(pythonCommand, [script, args]);
	sensor.stdout.on('data', function(data)
	{
		console.log(String(data))
		showQueryAndResultAsVsMessage(args, String(data));
	});
}

function getHelp()
{
	vscode.window.showInformationMessage(`for help click the arraw on this message 
	| c++ = c++:function:your question | java = java:library:your question 
	| python = pyhon:library:your question | python pandas = pandas:library/function:your question
	| python numpy = numpy:library/function:your question | python matplotlib = matplotlib:library/function:your question
	| rust = rust:library:your question`);
}

async function getUserInputAndExecuteQuery()
 {
	const pythonScript = 'terminal.py'
	const query = await vscode.window.showInputBox
	({
		value: 'proglanguage:lib:function or help for help',
		placeHolder: 'proglanguage:lib:function'
	});
	query === 'help' ? getHelp() : (query.split(':').length === 3) && (query !== 'proglanguage:lib:function') ? callPythonScript(pythonScript, query) : vscode.window.showInformationMessage("Error: wrong input try again");
 }

function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('started "codehelper"');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('extension.helloWorld', function () 
	{
		getUserInputAndExecuteQuery();
	});

	context.subscriptions.push(disposable);
}
exports.activate = activate;

// this method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
