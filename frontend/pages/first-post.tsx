import Link from 'next/link';
import Head from 'next/head';
import Script from 'next/script';
import Layout from '../components/layout';

import { useState, useEffect } from 'react'

import { useRouter } from 'next/router'


export default function FirstPost({ count }) {
    const [data, setData] = useState(null)
    const [isLoading, setLoading] = useState(false)

    const router = useRouter()
    const { pid } = router.query

    console.log('PID', pid)

    const sendData = {
        start_properties: {'route': 'web/test'},
        link_label: 'com.freelearning.base.NEXT_OF',
        end_entity_id: 844424930135849,
    }
    useEffect(() => {
        setLoading(true)
        fetch('http://localhost:8000/api/com.freelearning.base/v1/query-linked/', {
            method: 'POST',
            body: JSON.stringify(sendData),
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then((res) => res.json())
        .then((data) => {
            setData(data)
            setLoading(false)
        })
    }, [])

    if (isLoading) return <p>Loading...</p>
    if (!data) return <p>No profile data</p>

    return (
        <Layout>
            <style jsx>{`
        h1 {
          color: blue;
        }
        @media (max-width: 600px) {
          div {
            background: blue;
          }
        }
      `}</style>
        <Head>
            <title>First Post {count}</title>
            </Head>

    <div>
      <h1></h1>
      <p>{data.result[0][0].label}</p>
    </div>

        <h1>First Post</h1>
        <h2>
            <Link href="/">← Back to home</Link>
        </h2>
        </Layout>
    );
}
