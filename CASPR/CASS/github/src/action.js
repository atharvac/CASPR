const core = require("@actions/core");
const github = require("@actions/github");
// const util = require('util');
const openpgp = require('openpgp');
const fetch = require('node-fetch');


async function fetch_data(data, apiUrl, accessToken) {
    let headersSet = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Access-Token': accessToken
    }
    const resp = await fetch(apiUrl, {
        headers: headersSet,
        method: "POST",
        body: JSON.stringify(data)
    })
    return resp.json();
}


async function verifyCommit(publicKey, signatureData, messageData){
    let pubKeyLoaded = await openpgp.readKey({ armoredKey: publicKey });
    var createdMessage = await openpgp.createMessage({ text: messageData });
    const signature = await openpgp.readSignature({
        armoredSignature: signatureData // parse detached signature
    });
    const verificationResult = await openpgp.verify({
        message: createdMessage, // Message object
        signature: signature,
        verificationKeys: pubKeyLoaded
    });
    try{
        let verified = await verificationResult.signatures[0].verified;
        if (verified){
            return true;
        } else {
            throw new Error("Bad Signature!")
        }
    } catch (err){
        return false;
    }
}


async function getSignatureKeyID(signatureData){
    const signature = await openpgp.readSignature({
        armoredSignature: signatureData // parse detached signature
    });
    return signature.getSigningKeyIDs()[0].toHex();
}


async function run(){
    try{
        const GITHUB_TOKEN = core.getInput('GITHUB_TOKEN');
        const SERVER_API_URL = core.getInput('SERVER_API_URL');
        const ACCESS_TOKEN = core.getInput('ACCESS_TOKEN');
        const LOGGING_URL = SERVER_API_URL.split("api")[0] + "api/ci-status";

        const octokit = github.getOctokit(GITHUB_TOKEN);

        const { context = {} } = github;

        const ref = core.getInput("ref");
        core.info(`The head commit is: ${ref}`);
        var commit = await octokit.rest.git.getCommit({
            ...context.repo,
            commit_sha: ref
        });
        // core.info(util.inspect(commit, false, null, true));
        if (commit.data.verification.reason != "valid"){
            throw new Error("Authorization Failed!");
        }
        const payload = commit.data.verification.payload;
        try {
            var KeyID = await getSignatureKeyID(commit.data.verification.signature);
        } catch (error) {
            let logData = {
                "keyid": "No signature found!",
                "email": payload.match(/(?<=\<)[^\>[]*(?=>)/g)[0],
                "status": "failure"
            };
            let resp = await fetch_data(logData, LOGGING_URL, ACCESS_TOKEN);
            throw new Error("Signature not found!");
        }
        core.info("KeyID: " + KeyID);

        let data = {
            "keyid": KeyID
        }
        let api = SERVER_API_URL;
        let logData = {
            "keyid": KeyID,
            "email": payload.match(/(?<=\<)[^\>[]*(?=>)/g)[0]
        };

        let server_response = await fetch_data(data, api, ACCESS_TOKEN);
        if (server_response.status == "success"){
            let publicKey = server_response.data.publickey;
            let isVerified = await verifyCommit(
                publicKey,
                commit.data.verification.signature,
                commit.data.verification.payload
            )
            if (isVerified){
                logData["status"] = "success";
                core.info("Commit verified successfully!");
                let resp = await fetch_data(logData, LOGGING_URL, ACCESS_TOKEN);
            }
        }
        else {
            logData["status"] = "failure";
            let resp = await fetch_data(logData, LOGGING_URL, ACCESS_TOKEN);
            throw new Error(`\nServer rejected the key.`);
        }
        
    }
    catch (err) {
    // setFailed logs the message and sets a failing exit code
        core.setFailed(`Action failed with error ${err}`);
    }
}

run();