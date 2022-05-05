import { Heading, Flex, Stack, Input, Button, InputGroup, InputRightElement } from "@chakra-ui/react"
import { HiOutlineLogin, HiOutlineEye, HiOutlineEyeOff } from "react-icons/hi";
import React, { useState } from "react";

const Login = () => {
    // initialize states
    const [idInputValid, setIdInputValid] = useState(false)
    const [passwortInputValid, setPasswortInputValird] = useState(false)
    const [showPassword, setShowPassword] = useState(false)

    // verify login with backend
    // TODO: implement api call
    function login() {
        console.log('logging in...')
    }

    // validate user ID input
    function useridInput(event) {
        if (event.target.value !== "") {
            setIdInputValid(true)
        } else {
            setIdInputValid(false)
        }
    }

    // validate user password input
    function userPasswordInput(event) {
        if (event.target.value !== "") {
            setPasswortInputValird(true)
        } else {
            setPasswortInputValird(false)
        }
    }

    // invert show password status
    function showPasswordClicked() {
        setShowPassword(!showPassword)
    }

    return (
        <>
            <Flex align="center" justify='center'>
                <Flex justify="center" p="10" mt="20" w="40vw" maxW="400px" bg='white' rounded="2xl" flexFlow="column" shadow="xl">
                    {/* input fields */}
                    <Stack spacing={5}>
                        <Heading as="h3" textAlign="center">SoftDSim</Heading>
                        <Input type='text' placeholder='User ID' size='lg' bg='#efefef' onChange={useridInput} />
                        <InputGroup>
                            <Input type={showPassword ? 'text' : 'password'} placeholder='Password' size='lg' bg='#efefef' onChange={userPasswordInput} />
                            {/* show password */}
                            <InputRightElement h="full">
                                <Button size='xl' onClick={showPasswordClicked}>
                                    {showPassword ? <HiOutlineEyeOff /> : <HiOutlineEye />}
                                </Button>
                            </InputRightElement>
                        </InputGroup>
                    </Stack>
                    {/* login button */}
                    <Button rightIcon={<HiOutlineLogin />} colorScheme={idInputValid && passwortInputValid ? 'blue' : 'blackAlpha'} size='lg' mt="40px" onClick={login} isDisabled={idInputValid && passwortInputValid ? false : true}>
                        Login
                    </Button>
                </Flex>
            </Flex>
        </>

    )
}

export default Login;