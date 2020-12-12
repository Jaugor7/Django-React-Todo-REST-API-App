import React from 'react';
import './App.css';

class App extends React.Component{

  constructor(props)
  {
    super(props);
    this.state = {
      noteList : [],
      activeNote : {
        id : null,
        note: '',
      },
      edditing: false,
    }
    this.fetchNotes = this.fetchNotes.bind(this); 
    this.handleSubmit = this.handleSubmit.bind(this);
    this.getCookie = this.getCookie.bind(this);
    this.startEdit = this.startEdit.bind(this);
    this.deleteNote = this.deleteNote.bind(this);
  };

  getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


  componentWillMount()
  {
    this.fetchNotes();
  }

  fetchNotes()
  {
    console.log("Fetching...");
    fetch('http://localhost:8000/note/all/')
    .then(response => response.json())
    .then(data => 
      this.setState({
        noteList : data,
      })
    )
  }

  handleSubmit(e)
  {
    e.preventDefault()

    let csrftoken = this.getCookie('csrftoken');

    let text_data = document.getElementById("newNote").value
    
    console.log("Text:" ,text_data)

    let url = 'http://localhost:8000/create/'

    if(this.state.edditing == true)
    {
      url = `http://localhost:8000/update/${this.state.activeNote.id}`
      this.setState({
        edditing:false,
      })
    }

    fetch(url,{
      method:'POST',
      headers:{
        'Content-type':'application/json',
        'X-CSRFToken' : csrftoken,
      },
      body:JSON.stringify({
        note:text_data,
      })
    }).then((response)=> {
      this.fetchNotes()
      let form = document.getElementById('noteForm')
      form.reset()
      
    }).catch(function(error){
      console.log("Error:", error)
    })

  }

  startEdit(note){
    
    console.log(note)

    document.getElementById('newNote').value = note.note

    this.setState({
      activeNote: note,
      edditing: true,
    })

  }

  deleteNote(note){

    let csrftoken = this.getCookie('csrftoken');

    fetch(`http://localhost:8000/delete/${note.id}`, {
      method:'DELETE',
      headers:{
        'Content-type' : 'application/json',
        'X-CSRFToken': csrftoken,
      },
    }).then((response) => {
      this.fetchNotes()
    })
  }

  render(){

    let notes = this.state.noteList
    let self = this

    return(
      <div className="container">
        <header className="blog-header py-3">
          <div className="row flex-nowrap justify-content-between align-items-center">
            <div className="col-4 pt-1">
              <h3 className="title-color">Jaugor7</h3>
            </div>
            <div className="col-4 text-center">
              <a className="blog-header-logo text-dark" href="#"></a>
            </div>
            <div className="col-4 d-flex justify-content-end align-items-center">
              <a className="btn btn-outline-warning" href="http://localhost:8000/auth/logoutPage/">Logout</a>
            </div>
          </div>
        </header>

        <form onSubmit={this.handleSubmit} className="my-3" id="noteForm">
          <div className="form-row col-md-12 align-items-center justify-content-center">
            <div className="col-auto">
              <label className="sr-only" for="newNote">New Note...</label>
              <input type="text" className="noteInput form-control mb-2" name="note" id="newNote" placeholder="New Note..."/>
            </div>
            <div className="col-auto">
              <button type="submit" className="btn btn-outline-warning mb-2">Add</button>
            </div>
          </div>
        </form>

        <div className="row mx-auto col-md-11 flex justify-content-center">

          {notes.map((note, index)=>{

            return(

            <div key={note.id} className="card text-center m-2">
              <div className="card-body">
                <div className="float-right">
                  <button onClick={() => self.deleteNote(note) } type="button" className="close" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                  <button onClick={() => self.startEdit(note) } type="button" className="close" aria-label="Close">
                    <h6 class="card-subtitle my-1 mx-1">Edit</h6>
                  </button>
                </div>
                {console.log(note)}
            <h6 className="card-title text-left text-warning">{index+1}</h6>
                <p class="card-text">{note.note}</p>
              </div>
            </div>

            )
          })

          }
        </div>

        <footer className="blog-footer">
          <p><small>Discourse App Assignment By: (171312) Sudhansh Sharma (Jaypee University of Information Technology).</small></p>
          <p><small>Assignment Submission © Jaugor7</small></p>
      </footer>
    </div>  
    )
  }

}

export default App;
