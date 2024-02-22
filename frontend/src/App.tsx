import './App.css'

let pinecone_api:string;
let cohere_api:string;
let pinecone_index:string;
let mongodb_url:string;
let query:string;

function display_result(data) {
  document.getElementById("List").innerHTML = "";

  let list = document.getElementById("List");
  for (let i = 0; i < 10; ++i) {
    var li = document.createElement('li');
    li.innerText =  data['emails'][i]["Subject"] + "\n" + data['emails'][i]["Sender"] + "\n\n" + data['emails'][i]["Message"].substring(0, 700) + "...";
    list.appendChild(li);
 }

}

function postData() {
    display_info();
    fetch("http://localhost:5000/rag", {
      method: 'POST',
      headers: {'Content-Type' : 'application/json'},
      body: JSON.stringify({'query': query,
      'pinecone_api_key': pinecone_api, 
      'cohere_api_key': cohere_api, 
      'pinecone_index': pinecone_index,
      'mongodb_url': mongodb_url})
    }).then(res => res.json())
    .then(data => display_result(data));
  }

function fetchHandler() {
  query = (document.getElementById('query') as HTMLInputElement).value;
  if (query != ''){
    postData()
  }
  else {
    document.getElementById("List").innerHTML = "";

  }
}

function gatherHandler() {
  fetch("http://localhost:5000/get_emails", {
      method: 'POST',
      headers: {'Content-Type' : 'application/json'},
      body: JSON.stringify({'mongodb_url': mongodb_url})
    })
}

function display_info() {
  console.log(pinecone_api);
  console.log(cohere_api);
  console.log(mongodb_url);
  console.log(pinecone_index);
}

function submitHandler() {
  pinecone_api = (document.getElementById('pinecone_api') as HTMLInputElement).value;
  cohere_api = (document.getElementById('cohere_api') as HTMLInputElement).value;
  pinecone_index = (document.getElementById('pinecone_index') as HTMLInputElement).value;
  mongodb_url = (document.getElementById('mongodb_url') as HTMLInputElement).value;
  // display_info();
  (document.getElementById('configDialog') as HTMLFormElement).close();
}

function cancelHandler() {
  (document.getElementById('configDialog') as HTMLFormElement).close()
}

function App() {

    return <div>
    <h1><span className="me">Golden</span> <span className="ne">Retriever</span></h1>
    <textarea className='textarea1' id="query" rows={1} cols={33} placeholder='Query'/>
    <button className="fetchButton" role="button" onClick={fetchHandler}>Fetch</button>
    <button className="gatherButton" role="button" onClick={gatherHandler}>Gather Emails</button>


    <dialog className= 'configDialogs' id="configDialog">
    <div className="form" id="configForm">
      <div className="title">Configuration</div>
      <div className="pc_api">
        <input id="pinecone_api" className="input" type="password" placeholder=" " />
        <div className="cut"></div>
        <label htmlFor="password" className="placeholder"> PineCone API Key</label>
      </div>

      <div className="pc_index_name">
        <input id="pinecone_index" className="input" type="text" placeholder=" " />
        <div className="cut"></div>
        <label htmlFor="text" className="placeholder"> PineCone Index Name</label>
      </div>

      <div className="co_api">
        <input id="cohere_api" className="input" type="password" placeholder=" " />
        <div className="cut"></div>
        <label htmlFor="password" className="placeholder">Cohere API Key</label>
      </div>

      <div className="mongo_url">
        <input id="mongodb_url" className="input" type="text" placeholder=" " />
        <div className="cut cut-short"></div>
        <label htmlFor="text" className="placeholder">MongoDB URL</label>
      </div>

      <button className="submit" onClick={submitHandler}>Submit</button>
      <button className="cancel" onClick={cancelHandler}>Cancel</button>

    </div>
  </dialog>
  
<div className="content-container">
<div className="list-container">
  <ul id="List">
  </ul>
</div>
</div>
    <button className="configButton" onClick={() => (document.getElementById('configDialog') as HTMLDialogElement).showModal()}>Configure</button>

    </div>
}

export default App