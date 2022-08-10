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


async function run(signature, payload){
    try{
        var KeyID = await getSignatureKeyID(signature);
    } catch (e) {
        throw new Error("Could not find signature. Is the commit signed?")
    }
    // var KeyID = await getSignatureKeyID(signature);

    let accessToken = process.env.ACCESS_TOKEN;
    let commitSHA = process.env.CI_COMMIT_SHA;
    let apiUrl = process.env.SERVER_API_URL;

    let data = {
        "keyid": KeyID
    }
    let server_response = await fetch_data(data, apiUrl, accessToken);
    if (server_response.status != "success"){
        throw new Error(JSON.stringify(server_response));
    }
    let publicKey = server_response.data.publickey;
    console.log(publicKey)
    let isVerified = await verifyCommit(
        publicKey,
        signature,
        payload
    )
    console.log("Public Key:\n"+publicKey+"\n\n");
    console.log("Signature:\n"+signature+"\n\n");
    if (!isVerified){
        throw new Error("Could not verify commit!");
    }
    return "Verification Complete!";
}


function parseSignature(commitObject) {
    let signature = commitObject.substring(
        commitObject.indexOf("-----BEGIN PGP SIGNATURE-----"), 
        commitObject.lastIndexOf("-----END PGP SIGNATURE-----")
    );
    return signature+"\n-----END PGP SIGNATURE-----";
}


function parsePayload(commitObject){
    let payload = commitObject.substring(
        commitObject.indexOf("tree"), commitObject.indexOf("gpgsig")
    )
    payload += "\n" + commitObject.substring(
        commitObject.indexOf("-----END PGP SIGNATURE-----")+33,
        commitObject.length-1
    ) + "\n";
    return payload;
}


process.stdin.on('data', data => {
    let signature = parseSignature(data.toString());
    let payload = parsePayload(data.toString());

    run(signature, payload).then(res=>{
        console.log(res.toString());
    }).catch(err => {
        console.log(err.toString());
        console.log("Commit verification failed!")
        process.exit(1);
    });
});