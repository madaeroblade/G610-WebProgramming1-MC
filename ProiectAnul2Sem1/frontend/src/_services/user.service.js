import config from 'config';
import { authHeader } from '../_helpers';

config.apiUrl = "http://127.0.0.1:3010/api/v1";

export const userService = {
    login,
    logout,
    register,
    getAll,
    getById,
    update,
    delete: _delete
};

function login(username, password) {
    let formData = new FormData();
    formData.append("email", username);
    formData.append("password", password);

    const requestOptions = {
        method: 'POST',
        body: formData
    };

    return fetch(`${config.apiUrl}/login`, requestOptions)
        .then(handleResponse)
        .then(user => {
            // login successful if there's a jwt token in the response
            if (user.token) {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(user));
            }

            return user;
        });
}

function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
}

function register(user) {

    let formData = new FormData();
    formData.append("id_group", user.id_group);
    formData.append("firstname", user.firstName);
    formData.append("lastname", user.lastName);
    formData.append("email", user.username);
    formData.append("password", user.password);
    formData.append("job_title", user.job_title);

    const requestOptions = {
        method: 'PUT',
        body: formData,
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/users`, requestOptions).then(handleResponse);
}

function getAll() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/users`, requestOptions).then(handleResponse);
}


function getById(id) {
    let formData = new FormData();
    formData.append("id", id);

    const requestOptions = {
        method: 'GET',
        body: formData,
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/users`, requestOptions).then(handleResponse);
}

function update(user) {
    let formData = new FormData();
    formData.append("id_group", user.id_group);
    formData.append("firstname", user.firstName);
    formData.append("lastname", user.lastName);
    formData.append("email", user.username);
    formData.append("job_title", user.job_title);
    formData.append("id_user", user.id);

    const requestOptions = {
        method: 'POST',
        body: formData,
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/users`, requestOptions).then(handleResponse);
}

// prefixed function name with underscore because delete is a reserved word in javascript
function _delete(id) {
    let formData = new FormData();
    formData.append("id", id);

    const requestOptions = {
        method: 'DELETE',
        body: formData
        headers: authHeader()
    };

    return fetch(`${config.apiUrl}/users`, requestOptions).then(handleResponse);
}

function handleResponse(response) {
    return response.text().then(text => {
        const data = text && JSON.parse(text);
        if (!response.ok) {
            if (response.status === 401) {
                // auto logout if 401 response returned from api
                logout();
                location.reload(true);
            }

            const error = (data && data.message) || response.statusText;
            return Promise.reject(error);
        }

        return data;
    });
}