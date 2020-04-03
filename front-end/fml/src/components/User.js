import React, {useState} from 'react';
import 'semantic-ui-css/semantic.min.css';

const User = () => {
    const [teamId, setTeamId] = useState(2753605);
    const [playerList, setPlayerList] = useState([]);

    const onSubmit = async (e) => {
        e.preventDefault();
        const apiURL = `http://localhost:8000/user/${teamId}`;
        fetch(apiURL).then(function(response) {
            return response.json();
        }).then((response) => {
            console.log(response.gw)
        })
        .catch(function(e){
            console.log(e);
        });
    }
    return (
        <div>
            <form>
                <div className="ui large form">
                    <div className="one fields">
                        <div className="field">
                            <label>Enter your Team number</label>
                            <input
                                type="text"
                                className="column"
                                onChange={(e) => setTeamId(e.target.value)}
                                value={teamId}
                            />
                        </div>
                    </div>
                    <button id="submit-button"
                            onClick={onSubmit}
                            disabled={false}
                            className="primary ui submit button" 
                            type="submit" 
                            role="button" 
                            value="Submit">
                        Submit
                </button>

                </div> 
            </form>
        </div>
        
    );
}

export default User;