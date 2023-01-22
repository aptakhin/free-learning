import { useState } from "react"

export default function EmailAuth() {
    const [email, setEmail] = useState('')

    async function onSubmit(ev) {
        console.log('onSubmit', ev, email)

        const result = await fetch('https://learning.aptakhin.name/api/v1/auth/send-email', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'email': email,
            }),
        })
    }

    return <>
        <div class="py-12">
          <div class="mt-8 max-w-md">
            <div class="grid grid-cols-1 gap-1 m-8">

              <label class="block">Email:</label>
              <input type="email" class="
                mt-1
                block
                w-full
                rounded-md
                border-gray-300
                shadow-sm
                focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50
              " placeholder="john@example.com" onChange={ ev => setEmail(ev.target.value) }/>

                    <button class="rounded-full bg-lime-700" onClick={ onSubmit }>Go</button>
                </div>
            </div>
        </div>
    </>
}
