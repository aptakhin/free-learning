import Link from 'next/link';
import Head from 'next/head';
import Layout from '../../../components/layout';

import { useRouter } from 'next/router'
import useSWR from 'swr'

import React, { Suspense } from 'react';
import BaseEntityView from './baseEntityView';
import TextEditor from '../../../components/texteditor';


const fetcher = (param) => fetch(param.url, param.args).then(res => res.json())

const viewComponents = {
    'com.freelearning.base.entity': './baseEntityView',
}

function Loading() {
    return <h2>🌀 Loading...</h2>;
}

export default function View() {
    const router = useRouter()
    const { org, viewId } = router.query
    const entityId = viewId ? viewId : '0' // 844424930138471

    const sendData = {
        start_properties: {'route': 'web/test'},
        link_label: 'com.freelearning.base.NEXT_OF',
        end_entity_id: entityId,
    }
    const { data, error, isLoading } = useSWR(
        router.isReady? {
            url: 'http://localhost:8000/api/com.freelearning.base/v1/query-linked/',
            args: {
                method: 'POST',
                body: JSON.stringify(sendData),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        } : null, fetcher);

    const sendData2 = {
        link_label: 'com.freelearning.base.CHILD_OF',
        end_entity_id: entityId,
    }
    const { data: xdata, error: xerror, isLoading: isLoading2 } = useSWR(
        router.isReady? {
            url: 'http://localhost:8000/api/com.freelearning.base/v1/query-linked/',
            args: {
                method: 'POST',
                body: JSON.stringify(sendData2),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        } : null, fetcher);

    const loadingState = isLoading || isLoading2
    // if (loadingState) return <p>Loading</p>

    const rootItemData = data?.query_result?.[0]?.[2]
    const rootItem = <><BaseEntityView {...rootItemData} /> <TextEditor forRoot={true} onTextSubmit={(content) => onTextSubmit(content, org, rootItemData.id)}/></>

    async function onTextSubmit(content, org, replyTo) {
        console.log('FF', content, org, replyTo)

        const result = await fetch('http://localhost:8000/api/com.freelearning.base/v1/upsert-entity/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'typ': 'com.freelearning.base.entity',
                'subject_id': '',
                'properties': {
                    'title': '',
                    'main': {
                        'parser': {
                            'name': 'com.freelearning.base.markdown_parser',
                            'version': 1,
                        },
                        'content': content,
                        'blocks': [],
                    },
                    'addon': {
                        'blocks': [],
                    },
                }
            }),
        })

        const responseJson = await result.json()
        console.log('Fr', result, responseJson)
        // console.log(response);

        await fetch('http://localhost:8000/api/com.freelearning.base/v1/upsert-link/', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'typ': 'com.freelearning.base.CHILD_OF',
                'subject_id': '',
                'start_id': responseJson['id'],
                'end_id': replyTo,
                'text': '',
            }),
        })
    }

    const items2 = xdata?.query_result?.map((entry) => {
        const entity = entry[0]
        if (entity.label == "com.freelearning.base.entity") {
            return <><BaseEntityView {...entity} /> <TextEditor onTextSubmit={(content) => onTextSubmit(content, org, entity.id)}/></>
        } else if (entity.label == "com.freelearning.miro.entity") {
            return <MiroEntityView {...entity} />
        }
    })
    return (
        <Layout>

        <Head>
            <title>First Post</title>
            </Head>

            <div id='loadingState'>{loadingState}</div>
            <Suspense fallback={<Loading />}>

            <div>{rootItem}</div>
            <div>{items2}</div>

            </Suspense>
        </Layout>
    );
}
