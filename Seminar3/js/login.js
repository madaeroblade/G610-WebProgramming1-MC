document.addEventListener("DOMContentLoaded", () =>
{
    const signUpRef = document.getElementById('signUp');
    const signUpNameRef = document.getElementById('signUpName');
    const signUpEmailRef = document.getElementById('signUpEmail');
    const signUpBtnRef = document.getElementById('signUpBtn');
    const cancelBtnRef = document.getElementById('cancelBtn');
    const showPasswordBtnRef = document.getElementById('showPasswordBtn');
    const hidePasswordBtnRef = document.getElementById('hidePasswordBtn');
    const showPasswordConfirmBtnRef = document.getElementById('showPasswordConfirmBtn');
    const hidePasswordConfirmBtnRef = document.getElementById('hidePasswordConfirmBtn');
    const passwordInputRef = document.getElementById('passwordInput');
    const passwordInputConfirmRef = document.getElementById('passwordConfirmInput');
    const loginFormAlertRef = document.getElementById('loginFormAlert');

    showPasswordBtnRef.addEventListener('click', onShowPasswordBtnClick);
    hidePasswordBtnRef.addEventListener('click', onHidePasswordBtnClick);

    showPasswordConfirmBtnRef.addEventListener('click', onShowPasswordConfirmBtnClick);
    hidePasswordConfirmBtnRef.addEventListener('click', onHidePasswordConfirmBtnClick);

    signUpRef.addEventListener('submit', onSubmitFormClick);
    cancelBtnRef.addEventListener('click', onCancelFormClick);

    function onShowPasswordBtnClick()
    {
        showPasswordBtnRef.classList.toggle('hidden');
        hidePasswordBtnRef.classList.toggle('hidden');
        passwordInputRef.type = 'text';
    }

    function onHidePasswordBtnClick()
    {
        showPasswordBtnRef.classList.toggle('hidden');
        hidePasswordBtnRef.classList.toggle('hidden');
        passwordInputRef.type = 'password';
    }

    function onShowPasswordConfirmBtnClick()
    {
        showPasswordConfirmBtnRef.classList.toggle('hidden');
        hidePasswordConfirmBtnRef.classList.toggle('hidden');
        passwordInputConfirmRef.type = 'text';
    }

    function onHidePasswordConfirmBtnClick()
    {
        showPasswordConfirmBtnRef.classList.toggle('hidden');
        hidePasswordConfirmBtnRef.classList.toggle('hidden');
        passwordInputConfirmRef.type = 'password';
    }

    function onCancelFormClick()
    {
        console.log('Warning! You are about to reset your inputs. Are you sure you want to continue?');
        if (confirm('Warning! You are about to reset your inputs. Are you sure you want to continue?'))
        {
            signUpRef.reset();
        }
    }

    function onSubmitFormClick()
    {

        if (passwordInputRef.value != passwordInputConfirmRef.value)
        {
            loginFormAlertRef.innerHTML = 'You must confirm the entered password. The two passwords are not the same!';
            loginFormAlertRef.classList.toggle('hidden');

            return false;
        }
        else
        {
            loginFormAlertRef.classList.add('hidden');
            console.log('Congratulations! You have successfully created an account');
            let sum = 0;
            for (var i = 1; i < 50; i++)
            {
                sum = sum + i;
            }

            console.log(`Sum of all numbers up to 50: ${sum}`);

        }

        return false;
    }
});