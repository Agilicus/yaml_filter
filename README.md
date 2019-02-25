## yaml-filter

`yaml_filter [-i type,type] [-o type,type]`

Takes stdin, selects only objects in the 'in_filter', discards
objects in the 'out_filter', and writes the result to stdout.

The use case is with e.g. Kubernetes, you have a YAML file
which has CRD, webhook, and objects using these.

Apply the same YAML 3 times:

```
cat foo.yaml | yaml_filter -i CustomResourceDefinition | kubectl apply -f -
cat foo.yaml | yaml_filter -i ValidatingWebhookConfiguration | kubectl apply -f -
cat foo.yaml | kubectl apply -f -
```

on the last run you could choose

 -o CustomResourceDefinition,ValidatingWebhookConfiguration

to exclude those, but its a bit moot since Kubernetes will properly apply the unchanged
CRD and WebHook

## Rationale

Tools like `kustomize` re-order the input YAML. They are designed to
be run as `kustomize build . |kubectl apply -f -`. However, if you
are using a CustomResourceDefinition, or ValidatingWebhook, you
may have a specific order of input which must be achieved.

This tool allows you to run:

`kustomize build . | yaml_filter.py -i CustomResourceDefinition | kubectl apply -f -`
`kustomize build . | yaml_filter.py -i ValidatingWebhookConfiguration | kubectl apply -f -`
`kustomize build . | kubectl apply -f -`

