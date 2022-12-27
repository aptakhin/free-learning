import Link from 'next/link';
import Head from 'next/head';
import Script from 'next/script';
import Layout from '../../../components/layout';

import { useState, useEffect } from 'react'

import { useRouter } from 'next/router'


export default function FirstPost({ count }) {
    const [data, setData] = useState(null)
    const [data2, setData2] = useState(null)
    const [isLoading, setLoading] = useState(false)

    const router = useRouter()
    const { org, path } = router.query



    const entityId = path? path[1] : '0' // 844424930135849

    const sendData = {
        start_properties: {'route': 'web/test'},
        link_label: 'com.freelearning.base.NEXT_OF',
        end_entity_id: entityId,
    }

    const sendData2 = {
        link_label: 'com.freelearning.base.CHILD_OF',
        end_entity_id: entityId,
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
            // setLoading(false)
        })

        // setLoading(true)
        fetch('http://localhost:8000/api/com.freelearning.base/v1/query-linked/', {
            method: 'POST',
            body: JSON.stringify(sendData2),
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then((res) => res.json())
        .then((data) => {
            setData2(data)
            // setLoading(false)
        })
    }, [])

    console.log('PID', org, path, entityId, isLoading, data, data2)

    if (isLoading) return <p>Loading...</p>
    // if (!data) return <p>No profile data</p>
    if (!data2) return <p>No profile data</p>

    const items = data.result?.[0]?.map((entry) =>
        <li>MM: {entry.id}: {entry.label} {JSON.stringify(entry.properties)}</li>
    );

    const items2 = data2.result?.map((entry) =>
        <li>{entry[2].id}: {entry[2].label} {JSON.stringify(entry[2].properties)} -- {entry[1].id}: {entry[1].label} {JSON.stringify(entry[1].properties)} -- {entry[0].id}: {entry[0].label} {JSON.stringify(entry[0].properties)}</li>
    );


    if (isLoading) return <p>Loading...</p>
    // if (!data) return <p>No profile data</p>
    if (!data2) return <p>No profile data</p>

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
            <p>{items}</p>
            <p>{items2}</p>
        </div>

        <h1>First Post</h1>
        <h2>
            <Link href="/">← Back to home</Link>
        </h2>
        </Layout>
    );
}
