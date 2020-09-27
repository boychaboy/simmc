#!/bin/bash
if [[ $# -eq 0 ]] || [[ $# -eq 1 ]] || [[ $# -eq 2 ]]
then
	echo "run format > ./run_domain_keyword.sh [domain] [keyword]"
	exit 1

elif [[ $# -eq 3 ]]
then
	DOMAIN=$1
	KEYWORD=$2
	GPU_ID=$3
fi

VERSION=_p
PATH_DIR=$(realpath .)

# Generate sentences ("${DOMAIN}", multi-modal)
CUDA_VISIBLE_DEVICES=$GPU_ID python -m gpt2_dst.scripts.run_generation \
    --model_type=gpt2 \
    --model_name_or_path="${PATH_DIR}"/gpt2_dst/save/"${DOMAIN}"/"${KEYWORD}" \
    --num_return_sequences=1 \
    --length=100 \
    --gpu_id=$GPU_ID \
    --stop_token="<EOS>" \
    --num_beams=2 \
    --prompts_from_file="${PATH_DIR}"/gpt2_dst/data/"${DOMAIN}"/"${DOMAIN}"_devtest_dials_predict.txt \
    --path_output="${PATH_DIR}"/gpt2_dst/results/"${DOMAIN}"/"${KEYWORD}""${VERSION}"/"${DOMAIN}"_devtest_dials_predicted.txt

python -m gpt2_dst.utils.total_postprocess \
    --path="${PATH_DIR}"/gpt2_dst/results/"${DOMAIN}"/"${KEYWORD}""${VERSION}"/ \
    --domain="${DOMAIN}"


mv "${PATH_DIR}"/gpt2_dst/results/"${DOMAIN}"/"${KEYWORD}""${VERSION}"/"${DOMAIN}"_devtest_dials_predicted.txt "${PATH_DIR}"/gpt2_dst/results/"${DOMAIN}"/"${KEYWORD}""${VERSION}"/"${DOMAIN}"_devtest_dials_predicted.org

mv "${PATH_DIR}"/gpt2_dst/results/"${DOMAIN}"/"${KEYWORD}""${VERSION}"/"${DOMAIN}"_devtest_dials_predicted_processed.txt "${PATH_DIR}"/gpt2_dst/results/"${DOMAIN}"/"${KEYWORD}""${VERSION}"/"${DOMAIN}"_devtest_dials_predicted.txt